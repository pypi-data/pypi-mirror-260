import datetime
from uuid import UUID

import jsonpickle
import pymongo
from pymongo import database, results, errors

from aett.eventstore.EventStream import ICommitEvents, EventStream, IAccessSnapshots, Snapshot


# noinspection DuplicatedCode
class CommitStore(ICommitEvents):
    def __init__(self, db: database.Database, table_name='commits'):
        self.collection: database.Collection = db.get_collection(table_name)
        self.counters_collection: database.Collection = db.get_collection('counters')

    def get(self, bucket_id: str, stream_id: str, min_revision: int = 0,
            max_revision: int = 4_000_000_000) -> EventStream:
        max_revision = 4_000_000_000 if max_revision >= 4_000_000_000 else max_revision + 1
        min_revision = 0 if min_revision < 0 else min_revision
        filters = {"BucketId": bucket_id, "StreamId": stream_id}
        if min_revision > 0:
            filters['StreamRevision']: {'$gte': min_revision}
        if max_revision < 4_000_000_000:
            filters['StreamRevision']: {'$lte': max_revision}

        query_response: pymongo.cursor.Cursor = self.collection.find({'$and': [filters]})
        stream = EventStream.create(bucket_id, stream_id)
        commit_sequence = 0
        for doc in query_response.sort('CheckpointToken', direction=pymongo.ASCENDING):
            msgs = jsonpickle.decode(doc['Events'])
            for msg in msgs:
                stream.add(msg)
            commit_sequence = int(doc['CommitSequence'])
        stream.set_persisted(commit_sequence)
        return stream

    def commit(self, event_stream: EventStream, commit_id: UUID):
        try:
            ret = self.counters_collection.find_one_and_update(
                filter={'_id': 'CheckpointToken'},
                update={'$inc': {'seq': 1}}).get('seq')
            commit = event_stream.to_commit(commit_id)
            doc = {
                'BucketId': event_stream.bucket_id,
                'StreamId': event_stream.stream_id,
                'StreamRevision': commit.stream_revision,
                'CommitId': str(commit_id),
                'CommitSequence': commit.commit_sequence,
                'CommitStamp': int(datetime.datetime.now(datetime.UTC).timestamp()),
                'Headers': jsonpickle.encode(commit.headers),
                'Events': jsonpickle.encode(commit.events),
                'CheckpointToken': int(ret)
            }
            response: pymongo.results.InsertOneResult = self.collection.insert_one(doc)
        except Exception as e:
            if e.__class__.__name__ == 'ConditionalCheckFailedException':
                if self.detect_duplicate(commit_id, event_stream.bucket_id, event_stream.stream_id,
                                         event_stream.commit_sequence):
                    raise Exception(
                        f"Commit {commit_id} already exists in stream {event_stream.stream_id}")
                else:
                    event_stream.__update__(self)
                    return self.commit(event_stream, commit_id)
            else:
                raise Exception(
                    f"Failed to commit event to stream {event_stream.stream_id} with status code {e.response['ResponseMetadata']['HTTPStatusCode']}")

    def detect_duplicate(self, commit_id: UUID, bucket_id: str, stream_id: str, commit_sequence: int) -> bool:
        duplicate_check = self.collection.find_one(
            {'BucketId': bucket_id, 'StreamId': stream_id, 'CommitSequence': commit_sequence})
        return str(duplicate_check.get('CommitId')) == str(commit_id)


class SnapshotStore(IAccessSnapshots):
    def __init__(self, db: database.Database, table_name: str = 'snapshots'):
        self.collection: database.Collection = db.get_collection(table_name)

    def get(self, bucket_id: str, stream_id: str, version: int) -> Snapshot:
        try:
            item = self.collection.find_one(
                {'BucketId': bucket_id, 'StreamId': stream_id, 'StreamRevision': version})

            return Snapshot(bucket_id=item.get('BucketId'),
                            stream_id=item.get('StreamId'),
                            stream_revision=int(item.get('StreamRevision')),
                            payload=jsonpickle.decode(item.get('Payload')))
        except Exception as e:
            raise Exception(
                f"Failed to get snapshot for stream {stream_id} with status code {e.response['ResponseMetadata']['HTTPStatusCode']}")

    def add(self, snapshot: Snapshot):
        try:
            doc = {
                'BucketId': snapshot.bucket_id,
                'StreamId': snapshot.stream_id,
                'StreamRevision': snapshot.stream_revision,
                'Payload': jsonpickle.encode(snapshot.payload)
            }
            response = self.collection.insert_one(doc)
        except Exception as e:
            raise Exception(
                f"Failed to add snapshot for stream {snapshot.stream_id} with status code {e.response['ResponseMetadata']['HTTPStatusCode']}")


class PersistenceManagement:
    def __init__(self,
                 db: database.Database,
                 commits_table_name: str = 'commits',
                 snapshots_table_name: str = 'snapshots'):
        self.db: database.Database = db
        self.commits_table_name = commits_table_name
        self.snapshots_table_name = snapshots_table_name

    def initialize(self):
        try:
            counters_collection: database.Collection = self.db.create_collection('counters', check_exists=True)
            if counters_collection.count_documents({'_id': 'CheckpointToken'}) == 0:
                counters_collection.insert_one({'_id': 'CheckpointToken', 'seq': 0})
        except pymongo.errors.CollectionInvalid as e:
            pass
        try:
            commits_collection: database.Collection = self.db.create_collection(self.commits_table_name, check_exists=True)
            commits_collection.create_index([("BucketId", pymongo.ASCENDING), ("CheckpointNumber", pymongo.ASCENDING)],
                                            comment="GetFromCheckpoint", unique=True)
            commits_collection.create_index([("BucketId", pymongo.ASCENDING), ("StreamId", pymongo.ASCENDING),
                                             ("StreamRevisionFrom", pymongo.ASCENDING),
                                             ("StreamRevisionTo", pymongo.ASCENDING)], comment="GetFrom", unique=True)
            commits_collection.create_index([("BucketId", pymongo.ASCENDING), ("StreamId", pymongo.ASCENDING),
                                             ("CommitSequence", pymongo.ASCENDING)], comment="LogicalKey", unique=True)
            commits_collection.create_index([("CommitStamp", pymongo.ASCENDING)], comment="CommitStamp", unique=False)
            commits_collection.create_index([("BucketId", pymongo.ASCENDING), ("StreamId", pymongo.ASCENDING),
                                             ("CommitId", pymongo.ASCENDING)], comment="CommitId", unique=True)
        except pymongo.errors.CollectionInvalid as e:
            pass

        try:
            snapshots_collection: database.Collection = self.db.create_collection(self.snapshots_table_name,
                                                                                  check_exists=True)
            snapshots_collection.create_index([("BucketId", pymongo.ASCENDING), ("StreamId", pymongo.ASCENDING),
                                               ("StreamRevision", pymongo.ASCENDING)], comment="LogicalKey", unique=True)
        except pymongo.errors.CollectionInvalid as e:
            pass

    def drop(self):
        self.db.drop_collection(self.commits_table_name)
        self.db.drop_collection(self.snapshots_table_name)

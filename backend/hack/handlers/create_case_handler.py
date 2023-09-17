import logging

from fastapi import Depends
from pymongo.collection import Collection

from hack.api_models import CaseCreate, CaseRead
from hack.helper_functions import get_case_collection, get_case_revision_collection


class CreateCaseHandler:
    def __init__(
        self,
        case_collection: Collection = Depends(get_case_collection),
        revision_collection: Collection = Depends(get_case_revision_collection),
    ):
        self.revision_collection = revision_collection
        self.case_collection = case_collection

    def __call__(self, *args, **kwargs):
        return self

    def handle_by_case_number(self, data: CaseCreate) -> CaseRead:
        existing = self.case_collection.find_one({"case_number": data.case_number})
        return self._create_case(data, existing)

    def handle_by_id(self, data: CaseCreate) -> CaseRead:
        existing = self.case_collection.find_one({"_id": data.id})
        return self._create_case(data, existing)

    def _create_case(self, data: CaseCreate, existing: dict):
        # todo: Find one with projection
        # get current revision: todo: client could set revision for optimistic locking
        # TODO detect changes and only create revision if something changed
        if not existing:
            new_item = {**data.to_mongo(), **{"revision": 0}}
            created_case = self.case_collection.insert_one(new_item)

            composite_key = {"case_id": data.id, "revision": 0}
            self.revision_collection.insert_one({**new_item, **{"_id": composite_key}})
            case_id = new_item.pop("_id")

        else:
            current_revision = existing.get("revision", 0)
            next_revision = current_revision + 1
            new_item = {**data.to_mongo(), **{"revision": next_revision}}
            case_id = new_item.pop("_id")

            created_case = self.case_collection.update_one({"_id": existing["_id"]}, {"$set": new_item}, upsert=True)
            composite_key = {"case_id": data.id, "revision": next_revision}
            revision_item = {**new_item, **{"_id": composite_key}}
            self.revision_collection.insert_one(revision_item)
        # get current revision
        # update case entry and insert into records collection
        logging.info(created_case)
        return CaseRead.model_validate(new_item | {"id": case_id})

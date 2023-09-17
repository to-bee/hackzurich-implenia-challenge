import logging
import os
import time
from datetime import date
from typing import Annotated
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, FastAPI, File, HTTPException, Query
from pymongo.collection import Collection
from starlette.middleware.cors import CORSMiddleware

from hack.api_models import CaseCreate, CaseDetail, CaseRead, CaseStatus, MetabaseTheme, ReviewStatus
from hack.handlers.create_case_handler import CreateCaseHandler
from hack.helper_functions import get_case_collection, get_case_revision_collection, parse_date
from hack.service.gpt_import_service import GptImportService
from hack.service.question_service import QuestionService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cases/", tags=["Case"])
def read_question(
    status: CaseStatus = Query(default=None),
    case_collection: Collection = Depends(get_case_collection),
):
    filters = {}
    if status:
        filters["status"] = {"$eq": status}

    data = list(case_collection.find(filters))

    return [CaseRead.from_mongo(item) for item in data]


@app.get("/api/cases/{case_number}/summarize/", tags=["Case"])
def summarize_cases(
    case_number: int,
    case_collection: Collection = Depends(get_case_collection),
    service: QuestionService = Depends(QuestionService),
):
    case_data = case_collection.find_one({"case_number": case_number})
    case = CaseRead.from_mongo(case_data)
    record_data = [CaseRead.from_mongo(record) for record in case_collection.find({"case_number": case_number})]
    return service.summarize(case=case, records=record_data)


@app.post("/api/cases/import/text/", tags=["Case"])
def read_text(
    raw_data: str,
    service: GptImportService = Depends(GptImportService),
    handler: CreateCaseHandler = Depends(CreateCaseHandler),
) -> list[CaseRead]:
    structured_data: list[dict] = service.run_analyze_plaintext_content_task(input_data=raw_data)
    # structured_data = structured_data_read
    cases = []
    for item in structured_data:
        db_item = item | {
            "id": uuid4(),
            "start_date_proceeding": parse_date(item.get("start_date_proceeding")),
            "end_date_proceeding": parse_date(item.get("end_date_proceeding")),
            "interest_date": parse_date(item.get("interest_date")),
        }

        case: CaseRead = handler.handle_by_case_number(data=CaseCreate.model_validate(db_item))
        logging.info(f"Imported case: {case}")
        cases.append(case)
    return cases


@app.post("/api/cases/import/file/", tags=["Case"])
def read_file(
    file: Annotated[bytes, File()],
    service: GptImportService = Depends(GptImportService),
    handler: CreateCaseHandler = Depends(CreateCaseHandler),
) -> list[CaseRead]:
    raw_data = file.decode()
    structured_data: list[dict] = service.run_analyze_plaintext_content_task(input_data=raw_data)
    # structured_data = structured_data_read
    cases = []
    for item in structured_data:
        db_item = item | {
            "id": uuid4(),
            "start_date_proceeding": parse_date(item.get("start_date_proceeding")),
            "end_date_proceeding": parse_date(item.get("end_date_proceeding")),
            "interest_date": parse_date(item.get("interest_date")),
        }

        case: CaseRead = handler.handle_by_case_number(data=CaseCreate.model_validate(db_item))
        logging.info(f"Imported case: {case}")
        cases.append(case)
    return cases


@app.post("/api/cases/", tags=["Case"])
def create_case(case: CaseCreate):
    handler = CreateCaseHandler(case_collection=get_case_collection(), revision_collection=get_case_revision_collection())
    handler.handle_by_id(case)


@app.get("/api/cases/{id}", response_model=CaseDetail, tags=["Case"])
def read_case_by_id(
    id: UUID,
    case_revision_collection: Collection = Depends(get_case_revision_collection),
    case_collection: Collection = Depends(get_case_collection),
):
    current_case_data = case_collection.find_one({"_id": id})
    if not current_case_data:
        raise HTTPException(status_code=404, detail="Not found")

    revisions_data = case_revision_collection.find({"_id.case_id": id})

    revisions = [CaseRead.model_validate(_map_revision(record_item)) for record_item in revisions_data]

    return CaseDetail(current=CaseRead.from_mongo(current_case_data), revisions=revisions)


def _map_revision(revision):
    _id = revision.pop("_id")

    return {**revision, **{"id": _id["case_id"], "revision": _id["revision"]}}


@app.put("/api/cases/{id}/approve", tags=["Case"])
def approve_case(id: UUID):
    collection = get_case_collection()
    item = collection.find_one_and_update(filter={"_id": id}, update={"$set": {"review_status": ReviewStatus.ACCEPTED}})
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return CaseRead.from_mongo(item)


@app.put("/api/cases/{id}/decline", tags=["Case"])
def decline_case(id: UUID):
    collection = get_case_collection()
    item = collection.find_one_and_update(filter={"_id": id}, update={"$set": {"review_status": ReviewStatus.DECLINED}})
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return CaseRead.from_mongo(item)


@app.get("/api/metabase/{question_id}", tags=["Analytics"])
def get_metabase_url(
    question_id: int,
    type: str = Query(default="question"),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    theme: MetabaseTheme = Query(default=MetabaseTheme.TRANSPARENT),
):
    metabase_url = os.environ["METABASE_URL"]
    secret_key = os.environ["METABASE_SECRET_KEY"]

    # params = {
    #     "org_id": "my_org_id",
    # }
    # if start_date:
    #     params["start_date"] = start_date.isoformat()
    # if end_date:
    #     params["end_date"] = end_date.isoformat()
    params = {}
    payload = {
        "resource": {type: question_id},
        "params": params,
        "exp": round(time.time()) + (60 * 10),  # 10 minute expiration
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return f"{metabase_url}/embed/{type}/{token}#theme={theme.value}&bordered=false&titled=false"

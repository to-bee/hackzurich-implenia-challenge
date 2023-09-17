import json
import logging
import os
from pathlib import Path
from uuid import UUID

from pydantic_core import ValidationError
from pymongo.collection import Collection

from hack.api_models import CaseCreate
from hack.handlers.create_case_handler import CreateCaseHandler
from hack.helper_functions import current_file_cwd, get_case_collection, get_case_revision_collection, parse_date
from hack.service.gpt_import_service import GptImportService
from hack.service.pandas_import_service import PandasImportService

gpt_service = GptImportService()
pandas_service = PandasImportService()
file_data = []
case_revision_collection: Collection = get_case_revision_collection()
current_case_collection: Collection = get_case_collection()
handler = CreateCaseHandler(case_collection=current_case_collection, revision_collection=case_revision_collection)
data_dir = Path(current_file_cwd(__file__), "data/")


def import_from_gpt():
    all_data = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file not in [
                # "small_combined.txt"
                "1. Litigation_Report_Overview_Sample_Ltigation Report Group_2023.04.txt",
                "2. Litigation_Report_Overview_Sample_Litigation Report Group_2023.06.txt",
            ]:
                continue
            if file in [".DS_Store"]:
                continue
            file_path = Path(root, file)
            raw_data = open(file_path, "r").read()

            structured_data: list[dict] = gpt_service.run_analyze_plaintext_content_task(input_data=raw_data)
            all_data.extend(structured_data)
            for item in structured_data:
                db_item = item | {
                    "id": UUID(int=item["case_number"]),
                    "start_date_proceeding": parse_date(item.get("start_date_proceeding")),
                    "end_date_proceeding": parse_date(item.get("end_date_proceeding")),
                    "interest_date": parse_date(item.get("interest_date")),
                }

                created = handler.handle_by_case_number(data=CaseCreate.model_validate(db_item))
                print(f"Inserted imported: {created}")

    with open(Path(data_dir, "data.json").as_posix(), "w") as outfile:
        json.dump(all_data, outfile)


def to_bool(value: str | None):
    if not value:
        return False
    return value in ["yes", "true"]


def import_from_pandas():
    file_path = Path(data_dir, "import.xlsx")
    rows: list[dict] = pandas_service.import_data(file_path=file_path)
    for row in rows:
        row_data = row | dict(
            id=UUID(int=row["case_number"]),
            currency=row.pop("Currency", None),
            project_on_rda=to_bool(row.pop("project_on_rda", "false").lower()),
        )
        data = CaseCreate.model_validate(row_data)
        handler.handle_by_case_number(data=data)
        print("Sample imported")


def import_from_temp_file():
    structured_data = json.load(open(Path(data_dir, "data.json").as_posix(), "r"))
    for item in structured_data:
        try:
            db_item = item | {
                "id": UUID(int=item["case_number"]),
                "start_date_proceeding": parse_date(item.get("start_date_proceeding")),
                "end_date_proceeding": parse_date(item.get("end_date_proceeding")),
                "interest_date": parse_date(item.get("interest_date")),
            }

            data = CaseCreate.model_validate(db_item)
            handler.handle_by_case_number(data=data)
            print("Inserted imported")
        except ValidationError as e:
            logging.exception(e)


if __name__ == "__main__":
    import_from_pandas()
    # import_from_gpt()
    # import_from_temp_file()

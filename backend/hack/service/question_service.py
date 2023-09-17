import json
import logging
import os

import openai
from openai.openai_object import OpenAIObject

from hack.api_models import CaseRead
from hack.helper_functions import get_case_collection


class QuestionService:
    def __init__(
        self,
    ):
        super().__init__()
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def summarize(
        self,
        case: CaseRead,
        records: list[CaseRead],
    ) -> str:
        logging.info("Asking about related fields")

        def serialize_record(record):
            return "\n".join(
                [
                    f"Revision: {record.revision}",
                    f"Accumulated court costs: {record.accumulated_court_costs}",
                    f"Accumulated legal costs: {record.accumulated_legal_costs}",
                    f"Expected legal costs: {record.expected_court_costs}",
                    f"Real case cost: {record.real_case}",
                    f"Real case cost: {record.real_case}",
                    f"Value in dispute: {record.value_in_dispute}",
                ]
            )

        record_summary = "\n\n".join([serialize_record(record=case) for case in records])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a useful context summarizer."},
                {"role": "user", "content": f"Summarize the following litigation case: {case.sdict()}\n\nRecords: {record_summary}" ""},
            ],
            functions=[
                {
                    "name": "get_related_field_names",
                    "parameters": {
                        "type": "object",
                        "properties": {"summarized_case": {"type": "string", "description": "Summarization of the case"}},
                    },
                }
            ],
            function_call={"name": "get_related_field_names"},
        )
        response: OpenAIObject = response.choices[0].message
        return json.loads(response.function_call.arguments)["summarized_case"]

    def ask(
        self,
        input_data: list[CaseRead],
        question: str,
    ) -> list[dict]:
        if not input_data:
            logging.warning("Input data is empty. Skipping analysis")
            return []

        # context = json.dumps([case.sdict() for case in input_data])

        logging.info(["Requesting openai for prompt: ", input_data])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a useful assistant."},
                {"role": "user", "content": f"What fields are related to evaluate the question: '{question}'"},
            ],
            functions=[
                {
                    "name": "extract_useful_fields",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field_name": {"type": "string", "description": "Name of related_case_field", "enum": [field for field in CaseRead.model_fields]},
                                },
                            }
                        },
                    },
                }
            ],
            function_call={"name": "extract_useful_fields"},
        )
        response: OpenAIObject = response.choices[0].message
        return response


if __name__ == "__main__":
    case_data = get_case_collection().find_one({"case_number": 213})
    case = CaseRead.from_mongo(case_data)
    service = QuestionService()
    summary: str = service.summarize(case=case)
    print(summary)

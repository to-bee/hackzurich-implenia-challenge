import json
import logging
import os
from json import JSONDecodeError

import openai
from openai.openai_object import OpenAIObject

from hack.api_models import CaseStatus, CaseType, ClaimantRespondant, CountryCode, Currency, ProcessingStatus


class GptImportService:
    def __init__(
        self,
    ):
        super().__init__()
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def run_analyze_plaintext_content_task(self, input_data: str) -> list[dict]:
        if not input_data:
            logging.warning("Input data is empty. Skipping analysis")
            return []

        logging.info(["Requesting openai for prompt: ", input_data])
        response = openai.ChatCompletion.create(
            # https://platform.openai.com/docs/models/gpt-4
            # https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4
            # https://betterprogramming.pub/return-json-from-gpt-65d40bfc2ef6
            # model="gpt-3.5-turbo",
            model="gpt-3.5-turbo-16k",
            # model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with unstructured table, and your task is to extract all data out of it.",
                },
                {"role": "user", "content": input_data},
            ],
            functions=[
                {
                    "name": "extract_payables_of_unstructured_data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "object",
                                "properties": {
                                    "case_number": {"type": "number", "description": "Case number"},
                                    "business_unit": {"type": "string", "description": "Business unit / Division"},
                                    "project_description": {"type": "string", "description": "Project description"},
                                    "responsible": {"type": "string", "description": "Person responsible for the case"},
                                    "real_case": {"type": "number", "description": "Real case"},
                                    "considered_amount": {"type": "number", "description": "Considered amount"},
                                    "opportunities_risks": {"type": "number", "description": "Opportunities and Risks"},
                                    "accumulated_costs": {"type": "number", "description": "Accumulated costs"},
                                    "start_date_proceeding": {"type": "string", "description": "Start datetime of proceeding"},
                                    "end_date_proceeding": {"type": "string", "description": "End datetime of proceeding"},
                                    "interest_date": {"type": "string", "description": "Interest datetime"},
                                    "interest_rate_percent": {"type": "string", "description": "Interest rate in percent"},
                                    "implenia_share": {"type": "number", "description": "Implenia share"},
                                    "value_in_dispute": {"type": "number", "description": "Value in dispute"},
                                    "subject_matter": {"type": "string", "description": "Subject matter of the case"},
                                    "case_type": {"type": "string", "description": "Case type", "enum": [item for item in CaseType]},
                                    "case_status": {"type": "string", "description": "Status of the case", "enum": [item for item in CaseStatus]},
                                    "currency": {"type": "string", "description": "Currency used", "enum": [item for item in Currency]},
                                    "status_proceeding": {"type": "string", "description": "Status of the proceeding", "enum": [item for item in ProcessingStatus]},
                                    "country_party_relation": {"type": "string", "description": "Country code", "enum": [item for item in CountryCode]},
                                    "claimant_respondent": {"type": "string", "description": "Claimant or Respondent", "enum": [item for item in ClaimantRespondant]},
                                },
                            }
                        },
                    },
                }
            ],
            function_call={"name": "extract_payables_of_unstructured_data"},
        )

        response: OpenAIObject = response.choices[0].message
        print("Requesting openai done...")
        # JSONDecodeError will trigger a retry. Mostly an openai problem.
        raw_data = response.function_call.arguments
        try:
            prompt_result = json.loads(raw_data)
            return prompt_result["items"]
        except JSONDecodeError as e:
            print(raw_data)
            logging.exception(e)
            return []

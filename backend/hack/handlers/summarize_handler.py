import json
import logging
import os

import openai
from openai.openai_object import OpenAIObject


class SummarizeService:
    def __init__(
        self,
    ):
        super().__init__()
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def run_summarizing_task(self) -> None:
        pipeline_ocr_result: dict = record.pipeline_ocr_result
        input_data = "\n".join([batch["text"] for batch in pipeline_ocr_result])
        if not input_data:
            record.pipeline_status_summarize = PayablePipelineStatus.SKIPPED
            record.save()
        else:
            logging.info(["Requesting openai for prompt: ", input_data])
            response = openai.ChatCompletion.create(
                # https://platform.openai.com/docs/models/gpt-4
                # https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4
                # https://betterprogramming.pub/return-json-from-gpt-65d40bfc2ef6
                model="gpt-3.5-turbo-16k",
                # model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You will be provided with unstructured data, and your task is to extract data out of it.",
                    },
                    {"role": "user", "content": input_data},
                ],
                functions=[
                    {
                        "name": "extract_payable_unstructured_data",
                        "parameters": {
                            "type": "object",
                            "properties": get_record_properties(),
                        },
                    },
                ],
                function_call={"name": "extract_payable_unstructured_data"},
            )

            response: OpenAIObject = response.choices[0].message
            # JSONDecodeError will trigger a retry. Mostly an openai problem.
            prompt_result = json.loads(response.function_call.arguments)
            logging.info(["Saving prompt result: ", response.function_call.arguments])

            #
            # record.type = postprocess_document_type(value=prompt_result.get("payable_type"))
            #
            # record.amount = postprocess_amount(prompt_result)
            # record.amount_unit = prompt_result.get("amount_currency")
            #
            # record.date = parse_date(raw_date=prompt_result.get("iso_date"))
            #
            # record.pipeline_status_summarize = PayablePipelineStatus.SUCCESS
            # record.save()
            #

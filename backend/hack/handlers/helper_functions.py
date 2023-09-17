import logging
import re
from datetime import datetime

from dateutil.parser import ParserError, parse
from pydantic import ValidationError
from pydantic.types import Decimal


def get_record_properties():
    return {
        "amount": {
            "type": "string",
            "description": "Numeric amount, without currency, including VAT",
        },
        "amount_currency": {
            "type": "string",
            "description": "Amount currency",
        },
        "iso_date": {
            "type": "string",
            "description": "ISO date",
        },
        "title": {
            "type": "string",
            "description": "Title",
        },
        "services": {
            "type": "string",
            "description": "Rendered services",  # erbrachte Leistungen
        },
        "name": {
            "type": "string",
            "description": "Person or company name of the creditor",
        },
        "address": {
            "type": "string",
            "description": "Postal address of the creditor",
        },
        "email": {
            "type": "string",
            "description": "Email",
        },
        "phone": {
            "type": "string",
            "description": "Phone number",
        },
        "tax_number": {
            "type": "string",
            "description": "Tax number",
        },
        "iban": {
            "type": "string",
            "description": "IBAN",
        },
        "payment_reference": {
            "type": "string",
            "description": "Payment Reference",
        },
        "debitor_name": {
            "type": "string",
            "description": "Person or company name of the debitor",
        },
        "payable_type": {
            "type": "string",
            "description": 'Possible values: "receipt", "invoice", "other"',
        },
    }


def postprocess_amount(prompt_result):
    amount: str = prompt_result.get("amount")
    if not amount:
        return None

    # Convert European-style decimal numbers (1.234,56) to standard format (1234.56)
    if "." in amount and "," in amount:
        amount = amount.replace(".", "").replace(",", ".")
    # Convert commas to dots for numbers like 123,45
    else:
        amount = amount.replace(",", ".")

    amount = re.sub("[^0-9.]", "", amount)  # Only keep numbers and dots.

    try:
        return Decimal(amount)
    except ValidationError as e:
        logging.warning(f"{amount} is not a valid Decimal: {e.__str__()}")
        return None


def parse_date(raw_date: str) -> datetime | None:
    try:
        if not raw_date:
            return None
        return parse(raw_date)
    except (TypeError, ParserError):
        logging.warning(f'Could not parse "{raw_date}" into date.')
        return None


def postprocess_document_type(value: str) -> PayableRecordType | None:
    if payable_type_raw := value:
        lower_value = payable_type_raw.lower()
        try:
            return PayableRecordType(lower_value)
        except ValidationError as e:
            logging.warning(f"{lower_value} is not a valid PayableRecordType: {e.__str__()}")
            return None

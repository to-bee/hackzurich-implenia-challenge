from pathlib import Path

import pandas as pd


class PandasImportService:
    def _is_nan(self, input):
        if isinstance(input, str):
            return input == "nan"

        return pd.isnull(input)

    def import_data(self, file_path: Path) -> list[dict]:
        df = pd.read_excel(file_path)

        # Überprüfe, ob alle erforderlichen Spalten vorhanden sind
        required_columns = [
            "division",
            "business_unit",
            "country_party_relation",
            "ic",
            "investment_center_name",
            "psp",
            "project_description",
            "project_on_rda",
            "case_type",
            "responsible",
            "legal_responsible",
            "finance_responsible",
            "case_number",
            "claimant",
            "repondent_of_claim",
            "claimant_respondent",
            "status_proceeding",
            "subject_matter",
            "Currency",
            "value_in_dispute",
            "implenia_share_percent",
            "real_case",
            "considered_accounting",
            "opportunities_risks",
            "accumulated_legal_costs",
            "expected_legal_costs",
            "accumulated_court_costs",
            "expected_court_costs",
            "start_date_proceeding",
            "end_date_proceeding",
            "interest_date",
            "interest_rate_percent",
            "interests",
            "comments",
            "next_milestone",
            "date_next_milestone",
        ]

        rows = []
        for index, row in df.iterrows():
            row_data = {col: row[col] if not self._is_nan(row[col]) else None for col in required_columns}
            rows.append(row_data)

        return rows

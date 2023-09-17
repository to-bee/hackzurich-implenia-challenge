from datetime import datetime
from enum import Enum
from uuid import UUID

from hack.google_sdk.helper_models import StrictBaseModel


class ResponsibilityType(str, Enum):
    OWNER = "owner"
    REVIEWER = "reviewer"


class CaseStatus(str, Enum):
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    CLOSED = "closed"


class ReviewStatus(str, Enum):
    NEEDS_REVIEW = "needs_review"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class ProcessingStatus(str, Enum):
    FIRST_INSTANCE_EXCHANGE_OF_BRIEFS = "First Instance - Exchange of briefs"
    FIRST_INSTANCE_COURT_DELIBERATION = "First Instance - Court deliberation"
    EVIDENCE_PRESERVATION_PROCEEDINGS = "Evidence preservation proceedings (if not already otherwise pending)"
    SECOND_INSTANCE_EXCHANGE_OF_BRIEFS = "Second Instance - Exchange of briefs"
    BANKRUPTCY_PROCEEDINGS = "Bankruptcy proceedings"
    SECOND_INSTANCE_COURT_DELIBERATION = "Second Instance - Court deliberation"
    CONCILIATION_ADR_PROCEEDINGS = "Conciliation / ADR proceedings"


class CaseType(str, Enum):
    ACTIVE = "Legal case by Implenia"
    EXPECTED_ACTIVE = "Expected legal case by Implenia"
    PASSIVE = "Legal case against Implenia"
    EXPECTED_PASSIVE = "Expected legal case against Implenia"


class ClaimantRespondant(str, Enum):
    SUBCONTRACTOR = "subcontractor"
    CLIENT = "client"


class Responsibility(StrictBaseModel):
    user_id: UUID
    type: ResponsibilityType


class CaseUpdate(StrictBaseModel):
    pass


class LitigationType(Enum):
    PassiveExpected = 0
    ActiveExpected = 1
    Active = 2
    Passive = 3


CURRENCY_CHF = "CHF"
CURRENCY_EURO = "EUR"
CURRENCY_USD = "USD"


class Currency(str, Enum):
    CHF = "CHF"
    EURO = "EUR"
    USD = "USD"


class CountryCode(str, Enum):
    CH = "CH"
    DE = "DE"
    AT = "AT"
    IT = "IT"
    FR = "FR"
    US = "US"
    RO = "RO"
    NO = "NO"
    SE = "SE"


class Division(str, Enum):
    BUILDINGS = "buildings"
    CIVIL = "civil"
    REAL_ESTATE = "real_estate"
    SPECIAL_FOUNDATIONS = "special_foundations"
    TUNNELING = "tunneling"


class CaseCreate(StrictBaseModel):
    id: UUID
    case_number: int
    business_unit: str
    division: Division
    ic: str | int
    investment_center_name: str | int
    psp: int
    project_description: str
    project_on_rda: bool
    case_type: CaseType | str
    responsible: str
    legal_responsible: str
    finance_responsible: str
    real_case: float
    expected_legal_costs: float | None
    accumulated_legal_costs: float | None
    accumulated_court_costs: float | None
    expected_court_costs: float | None
    start_date_proceeding: datetime | None
    end_date_proceeding: datetime | None
    interest_date: datetime | None
    interest_rate_percent: str | float
    implenia_share_percent: float | None
    value_in_dispute: float | None
    currency: Currency | None
    subject_matter: str
    status_proceeding: ProcessingStatus | str | None
    country_party_relation: CountryCode | str | None
    claimant_respondent: ClaimantRespondant | str | None
    revision: int | None = None
    claimant: str
    repondent_of_claim: str
    considered_accounting: float
    opportunities_risks: float | None
    interests: float | None
    comments: str | None
    next_milestone: str | None
    date_next_milestone: str | datetime | None
    case_status: CaseStatus | str | None = None
    review_status: ReviewStatus | None = ReviewStatus.NEEDS_REVIEW


class CaseRead(CaseCreate):
    revision: int


class CaseDetail(CaseUpdate):
    current: CaseRead
    revisions: list[CaseRead]


class MetabaseTheme(str, Enum):
    DARK = "night"
    LIGHT = "light"
    TRANSPARENT = "transparent"

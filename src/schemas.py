from typing import Literal
from pydantic import BaseModel, Field

Category = Literal[
    "billing",
    "technical",
    "account",
    "cancellation_refund",
    "order_delivery",
    "general"
]

Priority = Literal["low", "medium", "high", "critical"]

ResolutionType = Literal[
    "self_service",
    "resolve",
    "escalate",
    "request_information"
]

class TicketTriage(BaseModel):
    category: Category = Field(description="Support ticket category")
    priority: Priority = Field(description="urgency of the ticket")
    language: str = Field(description="Language used in the customer ticket")

class BillingAnalysis(BaseModel):
    issue: str = Field(description="Short summary of the billing problem")
    amount: int = Field(description="Money amount mentioned, or 'unknown'")
    transaction_count: int = Field(description="Number of charges mentioned")
    refund_required: bool = Field(description="whether a refund is required")

class TechnicalAnalysis(BaseModel):
    issue: str = Field(description="Short summary of the technical problem")
    affected_feature: str = Field(description="Feature or area that is broken")
    error_message: str = Field(description="Error text if mentioned, else 'none'")
    troubleshoot_required: bool = Field(description="whether troubleshooting is still needed")

class AccountAnalysis(BaseModel):
    issue: str = Field(description="Short summary of the account problem")
    access_problem: bool = Field(description="whether login or access is blocked")
    verification_required: bool = Field(description="whether identity verification is needed")
    account_status: str = Field(description="likely account status for eg. active, locked or unknown")

class CancellationRefundAnalysis(BaseModel):
    request_type: str = Field(description="what the customer wants, for eg. cancel/refund/both")
    reason: str = Field(description="reason given by the customer")
    refund_required: bool = Field(description="whether a refund is needed or requested")
    retention_opportunity: str = Field(description="whether there may be a chance to retain the customer")

class OrderDeliveryAnalysis(BaseModel):
    issue: str = Field(description="short summary of the order/delivery problem")
    order_status: str = Field(description="current status of the order if mentioned, otherwise 'unknown'")
    delivery_problem: bool = Field(description="whether delivery is the main problem")
    customer_request: str = Field(description="what customer wants to be done")

class GeneralAnalysis(BaseModel):
    issue: str = Field(description="short summary of the customer problem")
    customer_request: str = Field(description="What the custome r is asking for")
    additional_context: bool = Field(description="any extra useful context from the ticket")

class ResolutionDecision(BaseModel):
    resolution_type: ResolutionType = Field(description="Chosen next step for the support system")
    recommended_action: str = Field(description="concrete action to take next")
    human_required: bool = Field(description="True if a human agent is needed")
    resolution_reason: str = Field(description="Why this resolution was chosen")

class TicketResult(BaseModel):
    ticket_id: str
    customer_name: str
    category: Category
    priority: Priority
    language: str
    case_summary: str
    resolution_type: str
    recommended_action: str
    human_required: bool
    resolution_reason: str
    response: str
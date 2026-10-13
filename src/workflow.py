from src.chains import (
    create_resolution_chain,
    create_response_chain,
    create_triage_chain,
    create_router
)
from src.schemas import TicketResult

CHAIN_LABELS = {
    "billing": "Billing Chain",
    "technical": "Technical Chain",
    "account": "Account Chain",
    "cancellation_refund": "Cancellation/Refund Chain",
    "order_delivery": "Order/Delivery Chain",
    "general": "General Chain",
}

def build_workflow(llm):
    return {
        "triage_chain": create_triage_chain(llm),
        "router": create_router(llm),
        "resolution_chain": create_resolution_chain(llm),
        "response_chain": create_response_chain(llm)
    }

def process_ticket(ticket, workflow):
    customer_name = ticket["customer_name"]
    ticket_text = ticket["ticket"]

    # stage1: Ticket Triage 
    triage = workflow["triage_chain"].invoke({
        "customer_name": customer_name,
        "ticket": ticket_text
    })

    print(f"Category: {triage.category}")
    print(f"Priority: {triage.priority}")
    print(f"Routing to: {CHAIN_LABELS.get(triage.category, 'General Chain')}")

    # stage2 & 3: Routing and Case Analysis
    case_analysis = workflow["router"].invoke({
        "category": triage.category,
        "customer_name": customer_name,
        "ticket": ticket_text
    })

    case_analysis_text = case_analysis.model_dump_json(indent=2)

    # stage4: Resolution Decision
    resolution = workflow["resolution_chain"].invoke({
        "category": triage.category,
        "customer_name": customer_name,
        "ticket": ticket_text,
        "priority": triage.priority,
        "language": triage.language,
        "case_analysis": case_analysis_text
    })

    print(f"Resolution: {resolution.resolution_type}")
    print(f"Human required: {'Yes' if resolution.human_required else 'No'}")

    # stage5: Response Generation
    response_text = workflow["response_chain"].invoke({
        "category": triage.category,
        "customer_name": customer_name,
        "ticket": ticket_text,
        "priority": triage.priority,
        "language": triage.language,
        "case_analysis": case_analysis_text,
        "resolution_type": resolution.resolution_type,
        "recommended_action": resolution.recommended_action,
        "human_required": resolution.human_required,
        "resolution_reason": resolution.resolution_reason
    })

    # stage6: Final Structured Output
    return TicketResult(
        ticket_id=ticket["ticket_id"],
        customer_name=customer_name,
        category=triage.category,
        priority=triage.priority,
        language=triage.language,
        case_summary=case_analysis_text,
        resolution_type=resolution.resolution_type,
        recommended_action=resolution.recommended_action,
        human_required=resolution.human_required,
        resolution_reason=resolution.resolution_reason,
        response=response_text.strip(),
    )
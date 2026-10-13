# AI Support Ticket Automation

A LangChain-based support workflow that reads customer tickets, classifies them, routes them to the right analysis path, decides an appropriate resolution, and drafts a customer-facing response.

This project uses Google Gemini through `langchain-google-genai` and structured outputs from Pydantic models to automate ticket triage and support handling.

## What it does

The application processes each support ticket in a multi-step pipeline:

1. Ticket triage
   - Identifies the category (`billing`, `technical`, `account`, `cancellation_refund`, `order_delivery`, `general`)
   - Determines priority (`low`, `medium`, `high`, `critical`)
   - Detects the language used in the ticket

2. Category-specific case analysis
   - Extracts key facts such as issue type, amount, affected feature, delivery status, or customer request
   - Uses structured schemas for each category

3. Resolution decision
   - Chooses one of:
     - `self_service`
     - `resolve`
     - `escalate`
     - `request_information`
   - Determines whether a human agent is required
   - Produces a recommended action and reasoning

4. Response generation
   - Drafts a final customer response in the detected language

5. Output persistence
   - Saves a structured JSON result for each processed ticket

## Project structure

```text
1_project/
├── app.py                     # Entry point for running the workflow
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── data/
│   ├── support_tickets.json  # Input support tickets
│   └── output/
│       └── support_ticket_results.json  # Generated results
├── prompts/
│   ├── classification_prompt.txt
│   ├── case_analysis_prompt.txt
│   ├── resolution_prompt.txt
│   └── response_prompt.txt
├── src/
│   ├── __init__.py
│   ├── chains.py              # LangChain chain definitions
│   ├── llm.py                # Gemini client setup
│   ├── schemas.py            # Structured output models
│   └── workflow.py           # End-to-end ticket processing workflow
└── README.md
```

## Tech stack

- Python
- LangChain
- Pydantic
- Google Gemini (`gemini-2.5-flash` by default)
- JSON output for ticket processing artifacts

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
copy .env.example .env
```

Then update `.env` with your Google Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Running the project

Execute:

```bash
python app.py
```

The application reads tickets from:

```text
data/support_tickets.json
```

and writes the processed outputs to:

```text
data/output/support_ticket_results.json
```

## Example input

Each ticket is expected to have:

```json
{
  "ticket_id": "TKT-1001",
  "customer_name": "Rahul Sharma",
  "ticket": "I was charged twice for my Premium subscription this month."
}
```

## Example output

Each processed result includes:

- `ticket_id`
- `customer_name`
- `category`
- `priority`
- `language`
- `case_summary`
- `resolution_type`
- `recommended_action`
- `human_required`
- `resolution_reason`
- `response`

## Notes

- The project is a practical demo of AI-driven customer support automation.
- It is designed for structured support ticket handling and can be extended to integrate with real ticketing systems, CRM tools, or human escalation workflows.
- Because it relies on an external LLM API, valid Gemini credentials are required for execution.

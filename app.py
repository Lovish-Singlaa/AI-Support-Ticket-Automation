import json
import sys
from pathlib import Path

from src.llm import create_llm
from src.workflow import build_workflow, process_ticket

PROJECT_ROOT = Path(__file__).resolve().parent

INPUT_FILE = PROJECT_ROOT/"data"/"support_tickets.json"
OUTPUT_FILE = PROJECT_ROOT/"data"/"output"/"support_ticket_results.json"

def load_tickets(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"Error: Input file not found: {path}")
        sys.exit(1)

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        print(f"Error: Invalid JSON in {path}: {error}")

    if not isinstance(tickets, list) or not tickets:
        print("Error: support_tickets must contain a non-empty list of tickets")
        sys.exit(1)

    return tickets

def save_results(file_path, results):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    serializable = [
        result.model_dump() if hasattr(result, "model_dump") else result
        for result in results
    ]

    with path.open("w", encoding="utf-8") as file:
        json.dump(serializable, file, indent=2, ensure_ascii=False)

    return path

def main():
    print("="*40)
    print("AI SUPPORT TICKET AUTOMATION")  
    print("="*40)
    print()

    tickets = load_tickets(INPUT_FILE)
    print(f"Loaded {len(tickets)} tickets from {INPUT_FILE.name}")
    print()

    llm = create_llm()
    workflow = build_workflow(llm)

    results = []

    for ticket in tickets:
        ticket_id = ticket.get("ticket_id", "UNKNOWN")
        print(f"Processing ticket: {ticket_id}")

        try:
            result = process_ticket(ticket, workflow)
            results.append(result)
        except Exception as error:
            print(f"Error while processing ticket -> {ticket_id}: {error}")
            print()
            continue
        print()

    if not results:
        print("No tickets were processed successfully")
        sys.exit(1)

    output_path = save_results(OUTPUT_FILE, results)

    print("="*40)
    print("Processing Completed")
    print("Results saved to: ")
    print(output_path.as_posix())
    print("="*40)

if __name__ == "__main__":
    main()
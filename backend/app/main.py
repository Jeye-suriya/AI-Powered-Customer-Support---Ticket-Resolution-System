from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.app.data.database import TicketDatabase
from backend.app.services.ticket_pipeline import TicketPipeline


app = FastAPI(
    title="AI-Powered Customer Support Ticket Resolution System",
    version="1.0.0"
)


pipeline = TicketPipeline()
database = TicketDatabase()


class TicketRequest(BaseModel):
    ticket: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Customer support ticket text."
    )


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/tickets")
def resolve_ticket(request: TicketRequest):
    ticket = request.ticket.strip()

    if not ticket:
        raise HTTPException(
            status_code=400,
            detail="Ticket cannot be empty."
        )

    try:
        return pipeline.process(ticket)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the ticket."
        )


@app.get("/api/tickets")
def get_ticket_history():
    try:
        return database.get_tickets()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve ticket history."
        )


@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    if ticket_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Ticket ID must be a positive integer."
        )

    try:
        ticket = database.get_ticket(ticket_id)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve ticket."
        )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found."
        )

    return ticket
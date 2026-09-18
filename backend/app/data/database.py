import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATABASE_PATH = BASE_DIR / "data" / "tickets.db"


class TicketDatabase:
    def __init__(self, database_path=DATABASE_PATH):
        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket TEXT NOT NULL,
                    status TEXT NOT NULL,
                    oos INTEGER NOT NULL,
                    oos_confidence REAL,
                    intent TEXT,
                    intent_confidence REAL,
                    response TEXT,
                    sources TEXT,
                    should_escalate INTEGER NOT NULL,
                    escalation_reasons TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def save_ticket(self, result):
        intent_data = result.get("intent") or {}
        oos_data = result.get("oos") or {}
        escalation_data = result.get("escalation") or {}

        sources = result.get("sources") or []
        escalation_reasons = (
            escalation_data.get("reasons") or []
        )

        created_at = datetime.now(
            timezone.utc  # noqa: UP017
        ).isoformat()

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tickets (
                    ticket,
                    status,
                    oos,
                    oos_confidence,
                    intent,
                    intent_confidence,
                    response,
                    sources,
                    should_escalate,
                    escalation_reasons,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.get("ticket", ""),
                    result.get("status", ""),
                    int(oos_data.get("is_oos", False)),
                    oos_data.get("confidence"),
                    intent_data.get("name"),
                    intent_data.get("confidence"),
                    result.get("response", ""),
                    json.dumps(sources),
                    int(
                        escalation_data.get(
                            "should_escalate",
                            False
                        )
                    ),
                    json.dumps(escalation_reasons),
                    created_at
                )
            )

            connection.commit()

            return cursor.lastrowid

    def get_tickets(self, limit=50):
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT *
                FROM tickets
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

        return [
            self._format_ticket(row)
            for row in rows
        ]

    def get_ticket(self, ticket_id):
        with self._connect() as connection:
            connection.row_factory = sqlite3.Row

            row = connection.execute(
                """
                SELECT *
                FROM tickets
                WHERE id = ?
                """,
                (ticket_id,)
            ).fetchone()

        if row is None:
            return None

        return self._format_ticket(row)

    def _format_ticket(self, row):
        return {
            "ticket_id": row["id"],
            "ticket": row["ticket"],
            "status": row["status"],
            "oos": {
                "is_oos": bool(row["oos"]),
                "confidence": row["oos_confidence"]
            },
            "intent": (
                {
                    "name": row["intent"],
                    "confidence": row["intent_confidence"]
                }
                if row["intent"]
                else None
            ),
            "response": row["response"],
            "sources": json.loads(
                row["sources"] or "[]"
            ),
            "escalation": {
                "should_escalate": bool(
                    row["should_escalate"]
                ),
                "reasons": json.loads(
                    row["escalation_reasons"] or "[]"
                )
            },
            "created_at": row["created_at"]
        }
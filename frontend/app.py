import json
import urllib.error
import urllib.request

import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="SupportAI",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state["page"] = "new_ticket"

if "ticket_result" not in st.session_state:
    st.session_state["ticket_result"] = None

if "selected_ticket_id" not in st.session_state:
    st.session_state["selected_ticket_id"] = None


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #F7F6F2;
    color: #172033;
}

.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background-color: transparent;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background-color: #172033;
    border-right: 1px solid #263047;
}

section[data-testid="stSidebar"] * {
    color: #E8E9EC;
}

.sidebar-brand {
    padding: 0.5rem 0 2.5rem 0;
}

.sidebar-brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #FFFFFF;
}

.sidebar-brand-line {
    width: 38px;
    height: 2px;
    background-color: #B59A62;
    margin-top: 0.6rem;
}

.sidebar-section {
    color: #8F99AA !important;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    margin-top: 1.5rem;
    margin-bottom: 0.65rem;
}

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 0.15rem;
}

section[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    border: 1px solid transparent !important;
    color: #D9DCE2 !important;
    text-align: left;
    padding: 0.55rem 0.65rem;
    font-size: 0.92rem;
    font-weight: 400;
    border-radius: 5px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #222C40 !important;
    border-color: #344057 !important;
    color: #FFFFFF !important;
}

.system-status {
    border-top: 1px solid #344057;
    margin-top: 2rem;
    padding-top: 1.2rem;
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.38rem 0;
    font-size: 0.78rem;
}

.status-name {
    color: #AEB5C1 !important;
}

.status-online {
    color: #9DBFA6 !important;
    font-weight: 600;
}

.status-ready {
    color: #C8B98C !important;
    font-weight: 600;
}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.main-header {
    margin-bottom: 2.5rem;
}

.eyebrow {
    color: #B59A62;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.main-title {
    color: #172033;
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin: 0;
}

.main-subtitle {
    color: #687386;
    font-size: 0.98rem;
    margin-top: 0.45rem;
}


/* ============================================================
   SECTIONS
   ============================================================ */

.section-label {
    color: #172033;
    font-size: 1.05rem;
    font-weight: 650;
    margin-bottom: 0.7rem;
}

.section-description {
    color: #687386;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}


/* ============================================================
   TICKET INPUT
   ============================================================ */

div[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #D8DBE1 !important;
    border-radius: 7px;
    font-size: 0.95rem;
    line-height: 1.6;
    padding: 1rem;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #B59A62 !important;
    box-shadow: 0 0 0 1px #B59A62 !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #9AA2AE !important;
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.stButton > button[kind="primary"] {
    background-color: #172033 !important;
    color: #FFFFFF !important;
    border: 1px solid #172033 !important;
    border-radius: 5px;
    padding: 0.65rem 1.4rem;
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}

.stButton > button[kind="primary"]:hover {
    background-color: #263047 !important;
    border-color: #263047 !important;
    color: #FFFFFF !important;
}


/* ============================================================
   CARDS
   ============================================================ */

.metric-card {
    background-color: #FFFFFF;
    border: 1px solid #E1E3E7;
    border-radius: 7px;
    padding: 1.1rem 1.2rem;
    min-height: 95px;
}

.metric-label {
    color: #7A8494;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

.metric-value {
    color: #172033;
    font-size: 1.05rem;
    font-weight: 650;
    word-break: break-word;
}

.response-card {
    background-color: #FFFFFF;
    border: 1px solid #E1E3E7;
    border-radius: 7px;
    padding: 1.4rem;
    line-height: 1.7;
    color: #303846;
}

.source-card {
    background-color: #FFFFFF;
    border: 1px solid #E1E3E7;
    border-radius: 7px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}

.source-title {
    color: #172033;
    font-weight: 650;
    font-size: 0.9rem;
}

.source-meta {
    color: #687386;
    font-size: 0.78rem;
    margin-top: 0.25rem;
}

.escalation-card {
    background-color: #FFFFFF;
    border: 1px solid #D8DBE1;
    border-left: 3px solid #B59A62;
    border-radius: 5px;
    padding: 1rem 1.2rem;
    color: #303846;
}

.history-card {
    background-color: #FFFFFF;
    border: 1px solid #E1E3E7;
    border-radius: 7px;
    padding: 1.15rem 1.25rem;
    margin-bottom: 0.7rem;
}

.history-ticket {
    color: #172033;
    font-size: 0.92rem;
    font-weight: 600;
    line-height: 1.5;
}

.history-meta {
    color: #687386;
    font-size: 0.78rem;
    margin-top: 0.45rem;
}

.empty-card {
    background-color: #FFFFFF;
    border: 1px dashed #D5D8DE;
    border-radius: 7px;
    padding: 2rem;
    text-align: center;
    color: #7A8494;
}

.premium-divider {
    height: 1px;
    background-color: #E1E3E7;
    margin: 2.2rem 0;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# API HELPERS
# ============================================================

def resolve_ticket(ticket: str):
    payload = json.dumps(
        {"ticket": ticket}
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{API_URL}/api/tickets",
        data=payload,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(
                error.read().decode("utf-8")
            ).get(
                "detail",
                "API request failed."
            )
        except Exception:
            detail = "API request failed."

        raise RuntimeError(detail) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Unable to connect to the support API. "
            "Make sure the FastAPI server is running."
        ) from error


def get_ticket_history():
    request = urllib.request.Request(
        f"{API_URL}/api/tickets",
        method="GET"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            "Unable to retrieve ticket history."
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Unable to connect to the support API. "
            "Make sure the FastAPI server is running."
        ) from error


def get_ticket(ticket_id):
    request = urllib.request.Request(
        f"{API_URL}/api/tickets/{ticket_id}",
        method="GET"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError:
        return None

    except urllib.error.URLError as error:
        raise RuntimeError(
            "Unable to connect to the support API."
        ) from error


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-name">SUPPORTAI</div>'
        '<div class="sidebar-brand-line"></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Dashboard",
        use_container_width=True,
        key="nav_dashboard"
    ):
        st.session_state["page"] = "dashboard"
        st.rerun()

    if st.button(
        "New Ticket",
        use_container_width=True,
        key="nav_new_ticket"
    ):
        st.session_state["page"] = "new_ticket"
        st.rerun()

    if st.button(
        "Ticket History",
        use_container_width=True,
        key="nav_history"
    ):
        st.session_state["page"] = "history"
        st.rerun()

    st.markdown(
        '<div class="sidebar-section">SYSTEM</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "System Status",
        use_container_width=True,
        key="nav_status"
    ):
        st.session_state["page"] = "status"
        st.rerun()

    st.markdown(
        '<div class="system-status">'
        '<div class="status-row">'
        '<span class="status-name">API</span>'
        '<span class="status-online">Online</span>'
        '</div>'
        '<div class="status-row">'
        '<span class="status-name">AI Pipeline</span>'
        '<span class="status-ready">Ready</span>'
        '</div>'
        '<div class="status-row">'
        '<span class="status-name">Knowledge Base</span>'
        '<span class="status-ready">Available</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state["page"] == "dashboard":

    st.markdown(
        '<div class="main-header">'
        '<div class="eyebrow">CUSTOMER SUPPORT PLATFORM</div>'
        '<div class="main-title">Dashboard</div>'
        '<div class="main-subtitle">'
        'Overview of the customer support resolution system.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        tickets = get_ticket_history()

        if isinstance(tickets, dict):
            tickets = tickets.get(
                "tickets",
                tickets.get("data", [])
            )

        if not isinstance(tickets, list):
            tickets = []

        total = len(tickets)

        resolved = sum(
            1
            for item in tickets
            if item.get("status") == "resolved"
        )

        escalated = sum(
            1
            for item in tickets
            if item.get("status") == "escalate"
        )

        out_of_domain = sum(
            1
            for item in tickets
            if item.get("status") == "out_of_domain"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Total Tickets</div>'
                f'<div class="metric-value">{total}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Resolved</div>'
                f'<div class="metric-value">{resolved}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Escalated</div>'
                f'<div class="metric-value">{escalated}</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Out of Domain</div>'
                f'<div class="metric-value">{out_of_domain}</div>'
                '</div>',
                unsafe_allow_html=True
            )

    except RuntimeError as error:
        st.error(str(error))


# ============================================================
# NEW TICKET
# ============================================================

elif st.session_state["page"] == "new_ticket":

    st.markdown(
        '<div class="main-header">'
        '<div class="eyebrow">CUSTOMER SUPPORT PLATFORM</div>'
        '<div class="main-title">AI Ticket Resolution</div>'
        '<div class="main-subtitle">'
        'Analyze customer issues, generate grounded responses, '
        'and route complex cases to support.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">New Support Ticket</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        "Enter the customer's issue below to begin the resolution process."
        '</div>',
        unsafe_allow_html=True
    )

    ticket = st.text_area(
        "Customer issue",
        placeholder="Describe the customer's issue...",
        height=170,
        label_visibility="collapsed",
        key="ticket_input"
    )

    st.write("")

    resolve_clicked = st.button(
        "Resolve Ticket",
        type="primary",
        key="resolve_ticket"
    )

    if resolve_clicked:

        if not ticket.strip():

            st.warning(
                "Please enter a customer issue before resolving the ticket."
            )

        else:

            with st.spinner(
                "Analyzing ticket and generating resolution..."
            ):

                try:

                    result = resolve_ticket(
                        ticket.strip()
                    )

                    st.session_state["ticket_result"] = result

                except RuntimeError as error:

                    st.error(str(error))


    st.markdown(
        '<div class="premium-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">Resolution</div>',
        unsafe_allow_html=True
    )

    result = st.session_state.get(
        "ticket_result"
    )

    if not result:

        st.markdown(
            '<div class="empty-card">'
            'Submit a ticket to view the AI resolution.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        intent = result.get(
            "intent"
        )

        status = result.get(
            "status",
            "unknown"
        )

        intent_name = (
            intent.get("name")
            if isinstance(intent, dict)
            else None
        )

        intent_confidence = (
            intent.get("confidence")
            if isinstance(intent, dict)
            else None
        )

        ticket_id = result.get(
            "ticket_id"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Ticket ID</div>'
                f'<div class="metric-value">'
                f'{ticket_id or "-"}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Status</div>'
                f'<div class="metric-value">'
                f'{status.replace("_", " ").title()}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Intent</div>'
                f'<div class="metric-value">'
                f'{intent_name or "Out of domain"}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col4:

            confidence_text = (
                f"{intent_confidence:.2%}"
                if isinstance(
                    intent_confidence,
                    (int, float)
                )
                else "-"
            )

            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-label">Intent Confidence</div>'
                f'<div class="metric-value">'
                f'{confidence_text}'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown(
            '<div class="section-label">AI Response</div>',
            unsafe_allow_html=True
        )

        response = result.get(
            "response",
            "No response generated."
        )

        response_html = (
            str(response)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

        st.markdown(
            f'<div class="response-card">'
            f'{response_html}'
            f'</div>',
            unsafe_allow_html=True
        )

        escalation = result.get(
            "escalation",
            {}
        )

        if escalation.get(
            "should_escalate",
            False
        ):

            reasons = escalation.get(
                "reasons",
                []
            )

            reason_text = "<br>".join(
                str(reason)
                for reason in reasons
            )

            st.write("")

            st.markdown(
                '<div class="section-label">Escalation</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="escalation-card">'
                '<strong>Human support required</strong>'
                '<br><br>'
                f'{reason_text}'
                '</div>',
                unsafe_allow_html=True
            )

        sources = result.get(
            "sources",
            []
        )

        if sources:

            st.write("")

            st.markdown(
                '<div class="section-label">Knowledge Sources</div>',
                unsafe_allow_html=True
            )

            for source in sources:

                similarity = source.get(
                    "similarity"
                )

                similarity_text = (
                    f"{similarity:.2%}"
                    if isinstance(
                        similarity,
                        (int, float)
                    )
                    else "-"
                )

                st.markdown(
                    '<div class="source-card">'
                    '<div class="source-title">'
                    f'{source.get("title", "Knowledge Base Article")}'
                    '</div>'
                    '<div class="source-meta">'
                    f'KB ID: {source.get("kb_id", "-")}'
                    '&nbsp;&nbsp;|&nbsp;&nbsp;'
                    f'Retrieval similarity: {similarity_text}'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


# ============================================================
# TICKET HISTORY
# ============================================================

elif st.session_state["page"] == "history":

    st.markdown(
        '<div class="main-header">'
        '<div class="eyebrow">CUSTOMER SUPPORT PLATFORM</div>'
        '<div class="main-title">Ticket History</div>'
        '<div class="main-subtitle">'
        'Review previously processed customer support tickets.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        tickets = get_ticket_history()

        if isinstance(tickets, dict):
            tickets = tickets.get(
                "tickets",
                tickets.get("data", [])
            )

        if not isinstance(tickets, list):
            tickets = []

        if not tickets:

            st.markdown(
                '<div class="empty-card">'
                'No tickets have been processed yet.'
                '</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<div class="section-label">'
                f'{len(tickets)} Ticket(s)'
                '</div>',
                unsafe_allow_html=True
            )

            for ticket_data in tickets:

                ticket_id = ticket_data.get(
                    "ticket_id",
                    ticket_data.get(
                        "id",
                        "-"
                    )
                )

                status = ticket_data.get(
                    "status",
                    "unknown"
                )

                intent = ticket_data.get(
                    "intent"
                )

                if isinstance(intent, dict):

                    intent_name = intent.get(
                        "name",
                        "-"
                    )

                else:

                    intent_name = intent or "-"

                ticket_text = ticket_data.get(
                    "ticket",
                    ticket_data.get(
                        "text",
                        "Ticket details unavailable."
                    )
                )

                created_at = ticket_data.get(
                    "created_at",
                    ticket_data.get(
                        "timestamp",
                        ""
                    )
                )

                ticket_html = (
                    str(ticket_text)
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                st.markdown(
                    '<div class="history-card">'
                    '<div class="history-ticket">'
                    f'Ticket #{ticket_id} — '
                    f'{ticket_html}'
                    '</div>'
                    '<div class="history-meta">'
                    f'Status: {status.replace("_", " ").title()}'
                    '&nbsp;&nbsp;|&nbsp;&nbsp;'
                    f'Intent: {intent_name}'
                    + (
                        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
                        f'Created: {created_at}'
                        if created_at
                        else ""
                    )
                    + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    f"View Ticket #{ticket_id}",
                    key=f"view_ticket_{ticket_id}"
                ):

                    st.session_state["selected_ticket_id"] = ticket_id
                    st.session_state["page"] = "ticket_detail"
                    st.rerun()

    except RuntimeError as error:

        st.error(str(error))


# ============================================================
# TICKET DETAIL
# ============================================================

elif st.session_state["page"] == "ticket_detail":

    ticket_id = st.session_state.get(
        "selected_ticket_id"
    )

    st.markdown(
        '<div class="main-header">'
        '<div class="eyebrow">CUSTOMER SUPPORT PLATFORM</div>'
        '<div class="main-title">Ticket Details</div>'
        '<div class="main-subtitle">'
        f'Resolution details for ticket #{ticket_id}.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if ticket_id is None:

        st.warning(
            "No ticket selected."
        )

    else:

        try:

            ticket_data = get_ticket(
                ticket_id
            )

            if ticket_data is None:

                st.error(
                    "Ticket not found."
                )

            else:

                ticket = ticket_data.get(
                    "ticket",
                    ticket_data.get(
                        "text",
                        "-"
                    )
                )

                status = ticket_data.get(
                    "status",
                    "unknown"
                )

                intent = ticket_data.get(
                    "intent"
                )

                if isinstance(intent, dict):

                    intent_name = intent.get(
                        "name",
                        "-"
                    )

                    intent_confidence = intent.get(
                        "confidence"
                    )

                else:

                    intent_name = intent or "-"
                    intent_confidence = None

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        '<div class="metric-card">'
                        '<div class="metric-label">Ticket ID</div>'
                        f'<div class="metric-value">'
                        f'{ticket_id}'
                        '</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        '<div class="metric-card">'
                        '<div class="metric-label">Status</div>'
                        f'<div class="metric-value">'
                        f'{status.replace("_", " ").title()}'
                        '</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                with col3:

                    confidence_text = (
                        f"{intent_confidence:.2%}"
                        if isinstance(
                            intent_confidence,
                            (int, float)
                        )
                        else "-"
                    )

                    st.markdown(
                        '<div class="metric-card">'
                        '<div class="metric-label">Intent Confidence</div>'
                        f'<div class="metric-value">'
                        f'{confidence_text}'
                        '</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                st.write("")

                st.markdown(
                    '<div class="section-label">Customer Ticket</div>',
                    unsafe_allow_html=True
                )

                ticket_html = (
                    str(ticket)
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                st.markdown(
                    f'<div class="response-card">'
                    f'{ticket_html}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.write("")

                st.markdown(
                    '<div class="section-label">Detected Intent</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="response-card">'
                    f'{intent_name}'
                    '</div>',
                    unsafe_allow_html=True
                )

                response = ticket_data.get(
                    "response"
                )

                if response:

                    st.write("")

                    st.markdown(
                        '<div class="section-label">AI Response</div>',
                        unsafe_allow_html=True
                    )

                    response_html = (
                        str(response)
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                        .replace("\n", "<br>")
                    )

                    st.markdown(
                        f'<div class="response-card">'
                        f'{response_html}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                escalation = ticket_data.get(
                    "escalation",
                    {}
                )

                if escalation.get(
                    "should_escalate",
                    False
                ):

                    reasons = escalation.get(
                        "reasons",
                        []
                    )

                    reason_text = "<br>".join(
                        str(reason)
                        for reason in reasons
                    )

                    st.write("")

                    st.markdown(
                        '<div class="section-label">Escalation</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        '<div class="escalation-card">'
                        '<strong>Human support required</strong>'
                        '<br><br>'
                        f'{reason_text}'
                        '</div>',
                        unsafe_allow_html=True
                    )

                sources = ticket_data.get(
                    "sources",
                    []
                )

                if sources:

                    st.write("")

                    st.markdown(
                        '<div class="section-label">'
                        'Knowledge Sources'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    for source in sources:

                        similarity = source.get(
                            "similarity"
                        )

                        similarity_text = (
                            f"{similarity:.2%}"
                            if isinstance(
                                similarity,
                                (int, float)
                            )
                            else "-"
                        )

                        st.markdown(
                            '<div class="source-card">'
                            '<div class="source-title">'
                            f'{source.get("title", "Knowledge Base Article")}'
                            '</div>'
                            '<div class="source-meta">'
                            f'KB ID: {source.get("kb_id", "-")}'
                            '&nbsp;&nbsp;|&nbsp;&nbsp;'
                            f'Retrieval similarity: {similarity_text}'
                            '</div>'
                            '</div>',
                            unsafe_allow_html=True
                        )

                st.write("")

                if st.button(
                    "Back to Ticket History",
                    key="back_to_history"
                ):

                    st.session_state["page"] = "history"
                    st.rerun()

        except RuntimeError as error:

            st.error(str(error))


# ============================================================
# SYSTEM STATUS
# ============================================================

elif st.session_state["page"] == "status":

    st.markdown(
        '<div class="main-header">'
        '<div class="eyebrow">CUSTOMER SUPPORT PLATFORM</div>'
        '<div class="main-title">System Status</div>'
        '<div class="main-subtitle">'
        'Current status of the support platform components.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">API</div>'
            '<div class="metric-value">Online</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">AI Pipeline</div>'
            '<div class="metric-value">Ready</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-label">Knowledge Base</div>'
            '<div class="metric-value">Available</div>'
            '</div>',
            unsafe_allow_html=True
        )
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"

START_KB_ID = 95


TRANSFER_KB = [
    {
        "category": "Transfers",
        "intent": "balance_not_updated_after_bank_transfer",
        "title": "Bank transfer balance not updated",
        "problem": "A bank transfer was completed, but the available account balance has not been updated yet.",
        "symptoms": "Bank transfer completed; balance still shows the previous amount; transferred funds are not visible in the account.",
        "resolution_steps": "1. Confirm that the bank transfer was submitted successfully.\n2. Check the transfer status and transaction details.\n3. Allow the normal processing time for the transfer to complete.\n4. If the transfer has completed but the balance is still incorrect, contact support with the transfer details.",
        "additional_information": "Bank transfers may take time to appear depending on the transfer method and processing status.",
        "escalation_condition": "Escalate if the transfer is confirmed completed but the account balance remains incorrect or the transfer cannot be located.",
    },
    {
        "category": "Transfers",
        "intent": "beneficiary_not_allowed",
        "title": "Beneficiary cannot be added or used",
        "problem": "A customer cannot add, select, or make a transfer to a beneficiary.",
        "symptoms": "Beneficiary cannot be added; beneficiary is unavailable; transfer to a beneficiary is blocked or rejected.",
        "resolution_steps": "1. Check that the beneficiary details are entered correctly.\n2. Confirm that the beneficiary is supported for the intended transfer.\n3. Retry the operation after correcting any invalid details.\n4. If the beneficiary remains unavailable, contact support.",
        "additional_information": "Beneficiary availability can depend on account, transfer, or recipient restrictions.",
        "escalation_condition": "Escalate if a valid beneficiary cannot be added or used after the customer has confirmed the details.",
    },
    {
        "category": "Transfers",
        "intent": "cancel_transfer",
        "title": "Cancel a transfer",
        "problem": "A customer wants to cancel a transfer.",
        "symptoms": "Customer sent a transfer by mistake; customer wants to stop or cancel a transfer.",
        "resolution_steps": "1. Check the current transfer status.\n2. If cancellation is available for the current status, follow the available cancellation process.\n3. If the transfer has already been processed, cancellation may no longer be possible.\n4. Contact support if the transfer needs urgent intervention.",
        "additional_information": "Whether a transfer can be cancelled depends on its current processing status.",
        "escalation_condition": "Escalate urgent cancellation requests or cases where the transfer cannot be cancelled through the available process.",
    },
    {
        "category": "Transfers",
        "intent": "declined_transfer",
        "title": "Transfer was declined",
        "problem": "A transfer was declined and could not be completed.",
        "symptoms": "Transfer declined; transfer rejected; transfer did not go through.",
        "resolution_steps": "1. Check the transfer status and any available failure information.\n2. Verify the recipient and transfer details.\n3. Correct any incorrect information and retry if appropriate.\n4. Contact support if the transfer continues to be declined.",
        "additional_information": "A declined transfer may require additional investigation when the reason is not clear from the transaction information.",
        "escalation_condition": "Escalate if repeated transfer attempts are declined or the reason for the decline cannot be resolved from the available information.",
    },
    {
        "category": "Transfers",
        "intent": "failed_transfer",
        "title": "Transfer failed",
        "problem": "A transfer failed before it could be completed.",
        "symptoms": "Transfer failed; transfer did not complete; transfer shows a failed status.",
        "resolution_steps": "1. Check the transfer status and transaction details.\n2. Verify the recipient and transfer information.\n3. Retry the transfer if the details are correct and retrying is allowed.\n4. Contact support if the transfer continues to fail.",
        "additional_information": "A failed transfer may require review when the failure reason is not available or repeated attempts fail.",
        "escalation_condition": "Escalate repeated transfer failures or cases where the customer cannot determine why the transfer failed.",
    },
    {
        "category": "Transfers",
        "intent": "pending_transfer",
        "title": "Transfer is pending",
        "problem": "A transfer remains pending and has not completed yet.",
        "symptoms": "Transfer pending; transfer is still processing; transfer has not completed.",
        "resolution_steps": "1. Check the transfer status and transaction details.\n2. Confirm that the recipient and transfer information are correct.\n3. Allow the normal processing time for the transfer.\n4. Contact support if the transfer remains pending beyond the expected processing period.",
        "additional_information": "Transfer processing times vary depending on the transfer method and destination.",
        "escalation_condition": "Escalate if the transfer remains pending beyond the expected processing period or requires manual investigation.",
    },
    {
        "category": "Transfers",
        "intent": "receiving_money",
        "title": "How to receive money",
        "problem": "A customer wants to know how another person can send money to their account.",
        "symptoms": "How can someone send money to me; how do I receive money; someone wants to transfer money to me; receiving a transfer.",
        "resolution_steps": "1. Identify the supported method for receiving money.\n2. Provide the sender with the required recipient details.\n3. Ask the sender to verify the recipient details before sending.\n4. Check the incoming transfer status if the expected money does not arrive.",
        "additional_information": "Receiving money is different from sending a transfer. The required recipient information depends on the supported receiving method.",
        "escalation_condition": "Escalate if an expected incoming transfer cannot be located or the customer cannot receive money using a supported method.",
    },
    {
        "category": "Transfers",
        "intent": "supported_transfer_countries",
        "title": "Countries supported for transfers",
        "problem": "A customer wants to know whether transfers are supported to or from a particular country.",
        "symptoms": "Which countries support transfers; can I transfer money to another country; is this country supported for transfers; international transfer availability.",
        "resolution_steps": "1. Identify the destination or source country.\n2. Check whether transfers involving that country are supported.\n3. Confirm the applicable transfer method and requirements.\n4. Do not initiate the transfer if the destination is unsupported.",
        "additional_information": "Country availability is a transfer-support question and may depend on the destination, source, and transfer method.",
        "escalation_condition": "Escalate if support for the requested country cannot be confirmed or the customer requires review for a restricted destination.",
    },
    {
        "category": "Transfers",
        "intent": "transfer_fee_charged",
        "title": "Transfer fee charged",
        "problem": "A customer was charged a fee for a transfer.",
        "symptoms": "Transfer fee; unexpected transfer charge; customer sees an additional fee associated with a transfer.",
        "resolution_steps": "1. Check the transfer transaction details.\n2. Identify the fee shown for the transfer.\n3. Review the applicable fee information for that transfer method.\n4. Contact support if the fee appears incorrect or unexpected.",
        "additional_information": "Transfer fees can depend on the transfer method and transaction.",
        "escalation_condition": "Escalate disputed or apparently incorrect transfer fees.",
    },
    {
        "category": "Transfers",
        "intent": "transfer_not_received_by_recipient",
        "title": "Recipient has not received the transfer",
        "problem": "A transfer was sent successfully, but the recipient has not received the funds.",
        "symptoms": "Recipient has not received money; transfer appears completed but recipient cannot see the funds.",
        "resolution_steps": "1. Check the transfer status and transaction details.\n2. Confirm the recipient information is correct.\n3. Allow the expected processing time for the transfer method.\n4. Contact support if the transfer is completed but the recipient still has not received the funds.",
        "additional_information": "Delivery time can depend on the transfer method and recipient bank or destination.",
        "escalation_condition": "Escalate when a transfer is confirmed completed but the recipient has not received the funds after the expected processing period.",
    },
    {
        "category": "Transfers",
        "intent": "transfer_timing",
        "title": "How long a transfer normally takes",
        "problem": "A customer is asking about the normal time required for a transfer to arrive or complete.",
        "symptoms": "How long does a transfer take; how quickly will a transfer arrive; normal transfer time; expected transfer duration; when should a transfer arrive.",
        "resolution_steps": "1. Identify the transfer method and destination.\n2. Check the expected processing time for that transfer type.\n3. Explain that the normal transfer time can vary by method and destination.\n4. If the customer is asking about a specific delayed transfer, check its current status instead.",
        "additional_information": "This article covers general transfer timing questions. A specific transfer that is already showing as pending should be handled as a pending transfer.",
        "escalation_condition": "Escalate if a specific transfer has exceeded its expected processing time and requires investigation.",
    },
]


def build():
    print("SUPPORTAI TRANSFER KB BUILDER")
    print("Loading existing knowledge base...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"Existing articles: {len(df)}")

    existing_intents = set(df["intent"].dropna().astype(str))

    new_rows = []
    next_id = START_KB_ID

    for article in TRANSFER_KB:
        intent = article["intent"]

        if intent in existing_intents:
            continue

        search_text = "\n".join(
            [
                article["title"],
                article["problem"],
                article["symptoms"],
                article["resolution_steps"],
                article["additional_information"],
                article["escalation_condition"],
            ]
        )

        new_rows.append(
            {
                "kb_id": f"KB{next_id:03d}",
                "category": article["category"],
                "intent": article["intent"],
                "title": article["title"],
                "problem": article["problem"],
                "symptoms": article["symptoms"],
                "resolution_steps": article["resolution_steps"],
                "additional_information": article["additional_information"],
                "escalation_condition": article["escalation_condition"],
                "search_text": search_text,
            }
        )

        next_id += 1

    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
        print(f"Transfer articles added: {len(new_rows)}")

    # Update the three retrieval-sensitive articles.
    updates = {
        "receiving_money": {
            "title": "How to receive money",
            "problem": "A customer wants to know how another person can send money to their account.",
            "symptoms": "How can someone send money to me; how do I receive money; someone wants to transfer money to me; receiving a transfer.",
            "resolution_steps": "1. Identify the supported method for receiving money.\n2. Provide the sender with the required recipient details.\n3. Ask the sender to verify the recipient details before sending.\n4. Check the incoming transfer status if the expected money does not arrive.",
            "additional_information": "Receiving money is different from sending a transfer. The required recipient information depends on the supported receiving method.",
            "escalation_condition": "Escalate if an expected incoming transfer cannot be located or the customer cannot receive money using a supported method.",
        },
        "supported_transfer_countries": {
            "title": "Countries supported for transfers",
            "problem": "A customer wants to know whether transfers are supported to or from a particular country.",
            "symptoms": "Which countries support transfers; can I transfer money to another country; is this country supported for transfers; international transfer availability.",
            "resolution_steps": "1. Identify the destination or source country.\n2. Check whether transfers involving that country are supported.\n3. Confirm the applicable transfer method and requirements.\n4. Do not initiate the transfer if the destination is unsupported.",
            "additional_information": "Country availability is a transfer-support question and may depend on the destination, source, and transfer method.",
            "escalation_condition": "Escalate if support for the requested country cannot be confirmed or the customer requires review for a restricted destination.",
        },
        "transfer_timing": {
            "title": "How long a transfer normally takes",
            "problem": "A customer is asking about the normal time required for a transfer to arrive or complete.",
            "symptoms": "How long does a transfer take; how quickly will a transfer arrive; normal transfer time; expected transfer duration; when should a transfer arrive.",
            "resolution_steps": "1. Identify the transfer method and destination.\n2. Check the expected processing time for that transfer type.\n3. Explain that the normal transfer time can vary by method and destination.\n4. If the customer is asking about a specific delayed transfer, check its current status instead.",
            "additional_information": "This article covers general transfer timing questions. A specific transfer that is already showing as pending should be handled as a pending transfer.",
            "escalation_condition": "Escalate if a specific transfer has exceeded its expected processing time and requires investigation.",
        },
    }

    for intent, update in updates.items():
        mask = df["intent"] == intent

        if not mask.any():
            raise ValueError(f"Intent not found: {intent}")

        for column, value in update.items():
            df.loc[mask, column] = value

        search_text = "\n".join(
            [
                update["title"],
                update["problem"],
                update["symptoms"],
                update["resolution_steps"],
                update["additional_information"],
                update["escalation_condition"],
            ]
        )

        df.loc[mask, "search_text"] = search_text

    df.to_csv(DATA_PATH, index=False)

    print(f"Updated articles: {len(df)}")
    print("TRANSFER KB UPDATE COMPLETED")


if __name__ == "__main__":
    build()
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"

START_KB_ID = 106


TOPUP_CASH_KB = [
    {
        "category": "Top Up",
        "intent": "automatic_top_up",
        "title": "Automatic top up",
        "problem": "A customer wants to automatically add money to their account.",
        "symptoms": "How do I enable automatic top up; where is auto top up; automatic top up limits.",
        "resolution_steps": "1. Open the available top up settings.\n2. Look for the automatic top up option.\n3. Configure the required amount or trigger if available.\n4. Review the configured limits before enabling automatic top up.",
        "additional_information": "Automatic top up availability and limits depend on the account and supported top up configuration.",
        "escalation_condition": "Escalate if the automatic top up option is unavailable when the customer expects it to be supported or configuration cannot be completed.",
    },
    {
        "category": "Cash and Cheque",
        "intent": "balance_not_updated_after_cheque_or_cash_deposit",
        "title": "Cash or cheque deposit not reflected in balance",
        "problem": "A cash or cheque deposit has been made but the account balance has not been updated.",
        "symptoms": "Cash deposit missing; cheque deposit pending; deposited cash not showing in balance; cheque has not updated the account.",
        "resolution_steps": "1. Confirm the deposit details and amount.\n2. Check whether the deposit has been processed.\n3. Allow the normal processing time for the deposit method.\n4. Contact support if the deposit remains missing after the expected processing period.",
        "additional_information": "Cash and cheque deposits may require processing before the balance is updated.",
        "escalation_condition": "Escalate if a confirmed cash or cheque deposit is still missing after the expected processing period.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "cash_withdrawal_charge",
        "title": "Cash withdrawal fee",
        "problem": "A customer was charged a fee when withdrawing cash.",
        "symptoms": "ATM fee; cash withdrawal charge; extra fee for withdrawing money.",
        "resolution_steps": "1. Check the cash withdrawal transaction details.\n2. Identify the fee associated with the withdrawal.\n3. Review the applicable withdrawal fee information.\n4. Contact support if the fee appears incorrect or unexpected.",
        "additional_information": "Cash withdrawal fees can depend on the withdrawal method, ATM, location, or applicable account conditions.",
        "escalation_condition": "Escalate disputed or apparently incorrect cash withdrawal fees.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "cash_withdrawal_not_recognised",
        "title": "Unrecognised cash withdrawal",
        "problem": "A customer sees a cash withdrawal they did not make.",
        "symptoms": "Unknown ATM withdrawal; cash withdrawal not recognised; someone withdrew cash using the account.",
        "resolution_steps": "1. Check the transaction details and withdrawal amount.\n2. Confirm whether the customer recognises the ATM transaction.\n3. Secure the account or card if unauthorised activity is suspected.\n4. Contact support immediately to report the unrecognised withdrawal.",
        "additional_information": "An unrecognised cash withdrawal may indicate unauthorised account or card activity.",
        "escalation_condition": "Escalate all reported unauthorised or unrecognised cash withdrawals for investigation.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "declined_cash_withdrawal",
        "title": "Cash withdrawal declined",
        "problem": "A customer attempted to withdraw cash but the ATM declined the transaction.",
        "symptoms": "ATM withdrawal declined; cannot withdraw cash; cash withdrawal rejected.",
        "resolution_steps": "1. Check the withdrawal details and available balance.\n2. Confirm that the card can be used for cash withdrawal.\n3. Try another supported ATM if appropriate.\n4. Contact support if cash withdrawals continue to be declined.",
        "additional_information": "Cash withdrawals can be declined for different account, card, ATM, or transaction reasons.",
        "escalation_condition": "Escalate repeated cash withdrawal declines when the customer cannot resolve the issue through normal checks.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "pending_cash_withdrawal",
        "title": "Cash withdrawal is pending",
        "problem": "A cash withdrawal is still showing as pending.",
        "symptoms": "ATM withdrawal pending; cash withdrawal still processing; pending cash transaction.",
        "resolution_steps": "1. Check the withdrawal transaction status.\n2. Confirm the withdrawal amount and ATM transaction details.\n3. Allow the normal processing time for the transaction.\n4. Contact support if the withdrawal remains pending beyond the expected period.",
        "additional_information": "A cash withdrawal can temporarily remain pending while the transaction is being processed.",
        "escalation_condition": "Escalate if the cash withdrawal remains pending beyond the expected processing period or requires transaction investigation.",
    },
    {
        "category": "Top Up",
        "intent": "pending_top_up",
        "title": "Top up is pending",
        "problem": "A top up has been initiated but is still showing as pending.",
        "symptoms": "Top up pending; top up still processing; money added but balance not updated.",
        "resolution_steps": "1. Check the top up transaction status.\n2. Confirm the top up amount and method.\n3. Allow the normal processing time for the top up.\n4. Contact support if the top up remains pending beyond the expected period.",
        "additional_information": "A top up may remain pending while the payment or funding method is being processed.",
        "escalation_condition": "Escalate if a top up remains pending beyond the expected processing period or requires transaction investigation.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_by_bank_transfer_charge",
        "title": "Fee for topping up by bank transfer",
        "problem": "A customer wants to know whether a fee applies when adding money by bank transfer.",
        "symptoms": "Bank transfer top up fee; SEPA transfer charge; fee for adding money by transfer.",
        "resolution_steps": "1. Identify the bank transfer method being used.\n2. Check the applicable fee information.\n3. Confirm any charges before initiating the transfer.\n4. Contact support if a charge appears inconsistent with the applicable fee information.",
        "additional_information": "Charges can depend on the bank transfer method and transaction.",
        "escalation_condition": "Escalate disputed or apparently incorrect bank transfer top up charges.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_by_card_charge",
        "title": "Fee for topping up by card",
        "problem": "A customer wants to know whether a fee applies when topping up using a card.",
        "symptoms": "Card top up fee; charge for topping up by card; top up card charges.",
        "resolution_steps": "1. Identify the card and top up method.\n2. Check the applicable card top up fee information.\n3. Review any charge before completing the top up.\n4. Contact support if the applied fee appears incorrect.",
        "additional_information": "Card top up charges can depend on the card, location, or supported top up method.",
        "escalation_condition": "Escalate disputed or apparently incorrect card top up charges.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_by_cash_or_cheque",
        "title": "Top up using cash or cheque",
        "problem": "A customer wants to add money using cash or a cheque.",
        "symptoms": "Top up with cash; top up with cheque; add money using a cheque; cash top up.",
        "resolution_steps": "1. Check whether cash or cheque top ups are supported.\n2. Review the available supported top up methods.\n3. Use a supported method to add money if cash or cheque deposits are unavailable.\n4. Contact support if the customer needs clarification about an available deposit method.",
        "additional_information": "Cash and cheque top ups depend on the supported funding methods available for the account.",
        "escalation_condition": "Escalate if the customer requires confirmation of a specific unsupported or unavailable cash or cheque deposit method.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_failed",
        "title": "Top up failed",
        "problem": "A customer attempted a top up but it failed or was rejected.",
        "symptoms": "Top up failed; top up rejected; top up not working; top up did not go through.",
        "resolution_steps": "1. Check the top up status and transaction details.\n2. Verify the selected top up method and entered information.\n3. Retry the top up if the details are correct and retrying is available.\n4. Contact support if the top up continues to fail.",
        "additional_information": "A failed top up may require investigation when the failure reason is unclear or repeated attempts fail.",
        "escalation_condition": "Escalate repeated top up failures or cases where the failure reason cannot be resolved.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_limits",
        "title": "Top up limits",
        "problem": "A customer wants to know the maximum amount they can add through top up.",
        "symptoms": "Maximum top up amount; top up limit; how much can I top up; increase top up limit.",
        "resolution_steps": "1. Check the applicable top up limits.\n2. Confirm the relevant top up method and account conditions.\n3. Ensure the requested amount is within the applicable limit.\n4. Contact support if the displayed limit appears incorrect.",
        "additional_information": "Top up limits can vary depending on the top up method and account conditions.",
        "escalation_condition": "Escalate if the customer cannot determine the applicable limit or a displayed limit appears incorrect.",
    },
    {
        "category": "Top Up",
        "intent": "top_up_reverted",
        "title": "Top up was reverted",
        "problem": "A completed or visible top up was later reversed or removed.",
        "symptoms": "Top up reverted; top up cancelled; money disappeared after top up; completed top up was reversed.",
        "resolution_steps": "1. Check the top up transaction status and history.\n2. Confirm the original top up amount and method.\n3. Check whether the transaction was reversed or cancelled.\n4. Contact support if the reversal is unexpected or the funds are missing.",
        "additional_information": "A top up may be reverted after initially appearing successful.",
        "escalation_condition": "Escalate unexpected top up reversals or cases where the funds have not been returned correctly.",
    },
    {
        "category": "Top Up",
        "intent": "topping_up_by_card",
        "title": "How to top up by card",
        "problem": "A customer wants to add money using a payment card.",
        "symptoms": "How do I top up with a card; add money using a credit or debit card; card top up.",
        "resolution_steps": "1. Open the top up option.\n2. Select the supported card top up method.\n3. Enter the required card and top up information.\n4. Confirm the top up and check the transaction status.",
        "additional_information": "Card top ups require a supported card and may be subject to applicable limits or verification.",
        "escalation_condition": "Escalate if a supported card cannot be used for top up or the top up cannot be completed after verification.",
    },
    {
        "category": "Top Up",
        "intent": "verify_top_up",
        "title": "Verify a top up",
        "problem": "A customer needs to verify a top up or asks about the verification code.",
        "symptoms": "Top up verification; verification code for top up; verify top up card.",
        "resolution_steps": "1. Check whether verification is requested for the top up.\n2. Follow the verification process shown for the transaction.\n3. Enter the required verification code when prompted.\n4. Contact support if the verification code is unavailable or does not work.",
        "additional_information": "Some top ups may require an additional verification step.",
        "escalation_condition": "Escalate if the required top up verification cannot be completed or the verification code is not accepted.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "wrong_amount_of_cash_received",
        "title": "Incorrect cash amount received",
        "problem": "A customer received a different amount of cash from the amount requested at an ATM.",
        "symptoms": "ATM gave less cash; wrong cash amount; partial cash withdrawal; cash received differs from requested amount.",
        "resolution_steps": "1. Check the ATM transaction amount.\n2. Confirm the amount requested and the physical cash received.\n3. Keep the transaction details and any ATM receipt.\n4. Contact support to report the cash amount discrepancy.",
        "additional_information": "The cash received can differ from the requested amount and may require transaction investigation.",
        "escalation_condition": "Escalate all reported discrepancies between the requested and received cash amounts.",
    },
    {
        "category": "Cash Withdrawal",
        "intent": "wrong_exchange_rate_for_cash_withdrawal",
        "title": "Wrong exchange rate for cash withdrawal",
        "problem": "A customer believes the exchange rate applied to a cash withdrawal was incorrect.",
        "symptoms": "Wrong ATM exchange rate; incorrect exchange rate for cash withdrawal; received less because of exchange rate.",
        "resolution_steps": "1. Check the cash withdrawal transaction details.\n2. Confirm the withdrawal currency and account currency.\n3. Review the exchange rate applied to the transaction.\n4. Contact support if the applied exchange rate appears incorrect.",
        "additional_information": "Exchange rates can affect the final account amount when withdrawing cash in another currency.",
        "escalation_condition": "Escalate disputed or apparently incorrect exchange rates applied to cash withdrawals.",
    },
]


def build():
    print("SUPPORTAI TOP UP / CASH KB BUILDER")
    print("Loading existing knowledge base...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"Existing articles: {len(df)}")

    existing_intents = set(df["intent"].dropna().astype(str))

    new_rows = []
    next_id = START_KB_ID

    for article in TOPUP_CASH_KB:
        intent = article["intent"]

        if intent in existing_intents:
            print(f"Skipping existing intent: {intent}")
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

    if not new_rows:
        print("No new top up/cash articles to add.")
        return

    updated_df = pd.concat(
        [df, pd.DataFrame(new_rows)],
        ignore_index=True,
    )

    updated_df.to_csv(DATA_PATH, index=False)

    print(f"Top up/cash articles added: {len(new_rows)}")
    print(f"Updated articles: {len(updated_df)}")
    print("TOP UP / CASH KB UPDATE COMPLETED")


if __name__ == "__main__":
    build()
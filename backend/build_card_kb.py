from pathlib import Path

import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

KB_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"


# ============================================================
# CARD / CARD-PAYMENT INTENTS
# ============================================================

CARD_INTENTS = {
    "card_arrival",
    "card_delivery_estimate",
    "card_linking",
    "card_not_working",
    "card_payment_fee_charged",
    "card_payment_not_recognised",
    "card_payment_wrong_exchange_rate",
    "card_swallowed",
    "card_acceptance",
    "lost_or_stolen_card",
    "activate_my_card",
    "card_about_to_expire",
    "change_pin",
    "compromised_card",
    "contactless_not_working",
    "getting_spare_card",
    "get_physical_card",
    "order_physical_card",
    "visa_or_mastercard",
}


# ============================================================
# ALIGNED CARD KB
# ============================================================

CARD_KB = [
    {
        "kb_id": "KB076",
        "category": "Cards",
        "intent": "card_arrival",
        "title": "Card has not arrived",
        "problem": (
            "The customer is waiting for a card that has already been "
            "ordered and has not arrived."
        ),
        "symptoms": (
            "Card delivery is taking longer than expected, the customer "
            "cannot find the card, or they want to track its delivery."
        ),
        "resolution_steps": (
            "Check the card delivery status and available tracking "
            "information. Confirm the delivery details associated with "
            "the order. If the card cannot be located or delivery appears "
            "to have failed, contact support for assistance."
        ),
        "additional_information": (
            "This intent concerns a card that has already been ordered "
            "and is expected to arrive."
        ),
        "escalation_condition": (
            "Escalate if the card cannot be located, delivery appears "
            "to have failed, or the customer reports a possible lost card."
        ),
        "search_text": (
            "card has not arrived card hasn't arrived waiting for card "
            "new card delivery delayed card delivery status track card "
            "where is my card card still waiting card lost during delivery"
        ),
    },
    {
        "kb_id": "KB077",
        "category": "Cards",
        "intent": "card_delivery_estimate",
        "title": "Card delivery estimate",
        "problem": (
            "The customer wants to know when a newly ordered card is "
            "expected to arrive or whether faster delivery is available."
        ),
        "symptoms": (
            "Questions about expected delivery date, delivery speed, "
            "fast tracking, or expedited delivery."
        ),
        "resolution_steps": (
            "Check the available card delivery options and the estimated "
            "delivery information for the customer's order."
        ),
        "additional_information": (
            "This intent concerns the expected delivery time rather than "
            "a card that is already overdue."
        ),
        "escalation_condition": (
            "Escalate if the expected delivery information is unavailable "
            "or the customer reports an overdue or failed delivery."
        ),
        "search_text": (
            "when will card arrive card delivery estimate delivery time "
            "how long card takes expected card delivery fast tracked card "
            "express delivery card delivery date"
        ),
    },
    {
        "kb_id": "KB078",
        "category": "Cards",
        "intent": "card_linking",
        "title": "Link a card to the app",
        "problem": (
            "The customer has a physical card and wants to link or add "
            "it to the app."
        ),
        "symptoms": (
            "Found card, new card not linked, card does not appear in "
            "the app, or customer wants to connect the card to the app."
        ),
        "resolution_steps": (
            "Open the card management area in the app and follow the "
            "available option to link or add the physical card."
        ),
        "additional_information": (
            "This intent concerns connecting an existing physical card "
            "to the customer's app."
        ),
        "escalation_condition": (
            "Escalate if the card cannot be linked after following the "
            "available in-app process."
        ),
        "search_text": (
            "link card app add card to app card not linked found card "
            "link physical card card show in app connect card app"
        ),
    },
    {
        "kb_id": "KB079",
        "category": "Cards",
        "intent": "card_not_working",
        "title": "Card is not working",
        "problem": (
            "The customer's card is not working when they attempt to use it."
        ),
        "symptoms": (
            "Card does not work, card is declined, or the customer "
            "cannot use the card generally."
        ),
        "resolution_steps": (
            "Check whether the problem occurs for multiple transactions "
            "or locations. Verify that the card is active and not blocked. "
            "If the problem continues, contact support for further checks."
        ),
        "additional_information": (
            "Use this intent for a general card problem when the customer "
            "has not identified a specific payment, contactless, ATM, "
            "or card-security issue."
        ),
        "escalation_condition": (
            "Escalate if the card remains unusable after basic checks "
            "or if there is a suspected security issue."
        ),
        "search_text": (
            "card not working card doesn't work card won't work unable "
            "to use card broken card card not usable card stopped working"
        ),
    },
    {
        "kb_id": "KB080",
        "category": "Card Payments",
        "intent": "card_payment_fee_charged",
        "title": "Fee charged for card payment",
        "problem": (
            "The customer was charged a fee when making a payment with "
            "their card."
        ),
        "symptoms": (
            "Unexpected card payment fee, extra fee when paying by card, "
            "or customer asks why a card payment has a charge."
        ),
        "resolution_steps": (
            "Review the payment and identify the fee shown in the "
            "transaction details. Explain the available fee information "
            "for that payment."
        ),
        "additional_information": (
            "This intent is specifically about a fee associated with "
            "a card payment."
        ),
        "escalation_condition": (
            "Escalate if the customer disputes the charge and the fee "
            "cannot be explained from the available transaction details."
        ),
        "search_text": (
            "card payment fee charged fee using card extra card payment "
            "charge card transaction fee payment fee charged"
        ),
    },
    {
        "kb_id": "KB081",
        "category": "Card Payments",
        "intent": "card_payment_not_recognised",
        "title": "Unrecognised card payment",
        "problem": (
            "The customer sees a card payment they do not recognise."
        ),
        "symptoms": (
            "Unknown merchant, unfamiliar card transaction, or a payment "
            "the customer says they did not make."
        ),
        "resolution_steps": (
            "Review the transaction details and merchant information. "
            "If the customer still does not recognise the payment, "
            "follow the available process for reporting an unrecognised "
            "card payment."
        ),
        "additional_information": (
            "Do not treat an unrecognised payment as a normal declined "
            "payment."
        ),
        "escalation_condition": (
            "Escalate when the customer reports an unauthorised or "
            "fraudulent card payment."
        ),
        "search_text": (
            "card payment not recognised unknown payment unfamiliar "
            "merchant card transaction I didn't make payment not mine "
            "unrecognised card charge unknown card payment"
        ),
    },
    {
        "kb_id": "KB082",
        "category": "Card Payments",
        "intent": "card_payment_wrong_exchange_rate",
        "title": "Wrong exchange rate for card payment",
        "problem": (
            "The customer believes the exchange rate applied to a "
            "card purchase was incorrect."
        ),
        "symptoms": (
            "Wrong exchange rate on purchase, incorrect currency "
            "conversion, or customer was charged more because of "
            "the exchange rate."
        ),
        "resolution_steps": (
            "Review the payment currency and exchange-rate information "
            "associated with the transaction. Compare the applied "
            "conversion information with the available transaction details."
        ),
        "additional_information": (
            "This intent concerns exchange rates applied to card payments, "
            "not general exchange-rate information."
        ),
        "escalation_condition": (
            "Escalate if the applied exchange rate appears incorrect "
            "and the transaction cannot be explained from the available data."
        ),
        "search_text": (
            "wrong exchange rate card payment purchase currency conversion "
            "exchange rate charged purchase exchange rate incorrect "
            "card purchase exchange rate"
        ),
    },
    {
        "kb_id": "KB083",
        "category": "Cards",
        "intent": "card_swallowed",
        "title": "Card retained by ATM",
        "problem": (
            "The customer's card was retained or swallowed by an ATM."
        ),
        "symptoms": (
            "ATM kept the card, card trapped inside ATM, or ATM did not "
            "return the card."
        ),
        "resolution_steps": (
            "Do not attempt to force the card out of the ATM. Follow the "
            "available card-replacement or card-security process and "
            "contact support if further assistance is required."
        ),
        "additional_information": (
            "This intent specifically concerns a physical card retained "
            "by an ATM."
        ),
        "escalation_condition": (
            "Escalate because the physical card has been retained by "
            "an ATM and may require replacement or security action."
        ),
        "search_text": (
            "ATM swallowed card ATM kept card card trapped ATM card not "
            "returned card retained by ATM machine took my card"
        ),
    },
    {
        "kb_id": "KB084",
        "category": "Cards",
        "intent": "card_acceptance",
        "title": "Where the card can be used",
        "problem": (
            "The customer wants to know which merchants, stores, or "
            "locations accept the card."
        ),
        "symptoms": (
            "Questions about card acceptance, supported businesses, "
            "stores, or places where the card can be used."
        ),
        "resolution_steps": (
            "Check the available card acceptance information for the "
            "type of transaction and merchant involved."
        ),
        "additional_information": (
            "This intent concerns where the card can be used rather than "
            "a specific declined transaction."
        ),
        "escalation_condition": (
            "Escalate if the customer reports a persistent acceptance "
            "problem that cannot be explained by the available information."
        ),
        "search_text": (
            "where can I use card card acceptance stores merchants "
            "businesses accept card card accepted locations card usage"
        ),
    },
    {
        "kb_id": "KB085",
        "category": "Cards",
        "intent": "lost_or_stolen_card",
        "title": "Lost or stolen card",
        "problem": (
            "The customer has lost their card or believes the card "
            "has been stolen."
        ),
        "symptoms": (
            "Lost card, stolen card, missing wallet containing the card, "
            "or request to replace a stolen card."
        ),
        "resolution_steps": (
            "Secure the missing card using the available card controls "
            "and follow the process for reporting and replacing a lost "
            "or stolen card."
        ),
        "additional_information": (
            "A missing physical card should be treated separately from "
            "an unrecognised payment."
        ),
        "escalation_condition": (
            "Escalate if the customer reports suspected fraudulent use "
            "of the missing card."
        ),
        "search_text": (
            "lost card stolen card missing card report stolen card "
            "replace stolen card lost wallet card missing physical card"
        ),
    },
    {
        "kb_id": "KB086",
        "category": "Cards",
        "intent": "activate_my_card",
        "title": "Card activation",
        "problem": (
            "The customer needs to activate a new card or reports that "
            "card activation is not working."
        ),
        "symptoms": (
            "Cannot activate card, new card needs activation, or "
            "activation attempt failed."
        ),
        "resolution_steps": (
            "Use the available card activation process in the app or "
            "through the supported activation method. If activation "
            "fails, contact support for assistance."
        ),
        "additional_information": (
            "Activation is separate from linking a card to the app."
        ),
        "escalation_condition": (
            "Escalate if the customer cannot activate the card after "
            "following the supported activation process."
        ),
        "search_text": (
            "activate card card activation activate new card card won't "
            "activate activation failed start using card"
        ),
    },
    {
        "kb_id": "KB087",
        "category": "Cards",
        "intent": "card_about_to_expire",
        "title": "Card expiration and replacement",
        "problem": (
            "The customer's card is approaching its expiration date "
            "and they want to know about replacement."
        ),
        "symptoms": (
            "Card expiring, expired card, replacement card, new expiration "
            "date, or replacement while abroad."
        ),
        "resolution_steps": (
            "Check the available replacement-card process and the "
            "customer's card status. Follow the supported replacement "
            "process for an expiring card."
        ),
        "additional_information": (
            "This intent concerns replacement of an expiring card."
        ),
        "escalation_condition": (
            "Escalate if the replacement cannot be arranged through "
            "the available process or the customer has a special "
            "replacement circumstance."
        ),
        "search_text": (
            "card expiring card about to expire expired card replacement "
            "new card expiration date replace expired card"
        ),
    },
    {
        "kb_id": "KB088",
        "category": "Cards",
        "intent": "change_pin",
        "title": "Change card PIN",
        "problem": (
            "The customer wants to change the PIN associated with "
            "their card."
        ),
        "symptoms": (
            "Request to change PIN, choose a different PIN, or ask "
            "where the PIN can be changed."
        ),
        "resolution_steps": (
            "Use the supported PIN-change process and follow the "
            "instructions provided for changing the card PIN."
        ),
        "additional_information": (
            "This intent concerns voluntarily changing the PIN. "
            "A blocked PIN is handled separately."
        ),
        "escalation_condition": (
            "Escalate if the customer cannot change the PIN using "
            "the supported process."
        ),
        "search_text": (
            "change PIN change pin number new PIN different PIN "
            "update card PIN modify PIN"
        ),
    },
    {
        "kb_id": "KB089",
        "category": "Card Security",
        "intent": "compromised_card",
        "title": "Card security compromise",
        "problem": (
            "The customer believes their card details or card have "
            "been compromised or used by someone else."
        ),
        "symptoms": (
            "Suspected fraudulent use, hacked card, stolen card details, "
            "or transactions the customer believes were made by someone else."
        ),
        "resolution_steps": (
            "Secure the card using the available controls and review "
            "the suspicious activity. Follow the supported process "
            "for reporting suspected card compromise."
        ),
        "additional_information": (
            "This intent concerns suspected compromise or fraudulent "
            "use, and should not be treated as an ordinary card problem."
        ),
        "escalation_condition": (
            "Escalate whenever the customer reports suspected fraudulent "
            "use or compromised card details."
        ),
        "search_text": (
            "compromised card hacked card fraudulent use card stolen "
            "card details someone using my card unauthorised card activity"
        ),
    },
    {
        "kb_id": "KB090",
        "category": "Cards",
        "intent": "contactless_not_working",
        "title": "Contactless payment not working",
        "problem": (
            "The customer cannot make a contactless payment with their card."
        ),
        "symptoms": (
            "Contactless payments fail, contactless does not work, "
            "or contactless payment is rejected."
        ),
        "resolution_steps": (
            "Try the supported contactless troubleshooting steps and "
            "check whether the physical card works through another "
            "supported payment method. If contactless remains unavailable, "
            "contact support."
        ),
        "additional_information": (
            "Use this intent for contactless-specific problems rather "
            "than general card payment declines."
        ),
        "escalation_condition": (
            "Escalate if contactless remains unavailable after "
            "supported troubleshooting."
        ),
        "search_text": (
            "contactless not working contactless payment fails "
            "tap payment doesn't work contactless card payment "
            "contactless rejected"
        ),
    },
    {
        "kb_id": "KB091",
        "category": "Cards",
        "intent": "getting_spare_card",
        "title": "Additional or spare card",
        "problem": (
            "The customer wants an additional physical card."
        ),
        "symptoms": (
            "Request for spare card, extra card, additional physical "
            "card, or questions about additional-card charges."
        ),
        "resolution_steps": (
            "Check the available options for ordering an additional "
            "physical card and any applicable information shown by "
            "the supported ordering process."
        ),
        "additional_information": (
            "This intent concerns an additional card rather than "
            "the customer's first physical card."
        ),
        "escalation_condition": (
            "Escalate if the additional-card request cannot be completed "
            "through the supported process."
        ),
        "search_text": (
            "spare card extra card additional card second card "
            "more physical cards additional card charge"
        ),
    },
    {
        "kb_id": "KB092",
        "category": "Cards",
        "intent": "get_physical_card",
        "title": "Physical card information",
        "problem": (
            "The customer is asking for information about obtaining "
            "or using a physical card."
        ),
        "symptoms": (
            "Questions about a physical card, including basic physical "
            "card information."
        ),
        "resolution_steps": (
            "Provide the available information about physical cards "
            "and direct the customer to the supported card-ordering "
            "process when they want to obtain one."
        ),
        "additional_information": (
            "The training data for this intent contains some noisy "
            "PIN-related examples, so this KB entry focuses on the "
            "physical-card meaning of the intent."
        ),
        "escalation_condition": (
            "Escalate if the customer's physical-card request cannot "
            "be handled through the supported process."
        ),
        "search_text": (
            "physical card get physical card physical bank card "
            "card information obtain physical card"
        ),
    },
    {
        "kb_id": "KB093",
        "category": "Cards",
        "intent": "order_physical_card",
        "title": "Order a physical card",
        "problem": (
            "The customer wants to order or request a physical card."
        ),
        "symptoms": (
            "Questions about requesting a card, physical card cost, "
            "or where a physical card can be delivered."
        ),
        "resolution_steps": (
            "Use the supported physical-card ordering process and "
            "review the available delivery and pricing information "
            "before submitting the order."
        ),
        "additional_information": (
            "This intent is specifically about placing an order for "
            "a physical card."
        ),
        "escalation_condition": (
            "Escalate if the customer cannot place the order through "
            "the supported process."
        ),
        "search_text": (
            "order physical card request card get card physical card "
            "card cost card price card delivery order new card"
        ),
    },
    {
        "kb_id": "KB094",
        "category": "Cards",
        "intent": "visa_or_mastercard",
        "title": "Visa or Mastercard",
        "problem": (
            "The customer wants to know whether the card is Visa or "
            "Mastercard or whether a preferred card network is available."
        ),
        "symptoms": (
            "Questions about Visa versus Mastercard and preference "
            "for a particular card network."
        ),
        "resolution_steps": (
            "Check the available card-network options and provide "
            "the applicable information for the customer's card."
        ),
        "additional_information": (
            "This intent concerns the card network, not general "
            "card acceptance."
        ),
        "escalation_condition": (
            "Escalate if the customer has a card-network request "
            "that cannot be handled through the available options."
        ),
        "search_text": (
            "visa mastercard Visa or Mastercard card network "
            "mastercard card visa card choose mastercard"
        ),
    },
]


# ============================================================
# VALIDATION
# ============================================================

def validate_card_kb():
    expected = len(CARD_INTENTS)
    actual = len(CARD_KB)

    if actual != expected:
        raise ValueError(
            f"Expected {expected} card KB entries, found {actual}."
        )

    intents = [
        row["intent"]
        for row in CARD_KB
    ]

    if set(intents) != CARD_INTENTS:
        missing = CARD_INTENTS - set(intents)
        extra = set(intents) - CARD_INTENTS

        raise ValueError(
            f"Intent mismatch. Missing={missing}, Extra={extra}"
        )

    if len(intents) != len(set(intents)):
        raise ValueError(
            "Duplicate card intents detected."
        )


# ============================================================
# UPDATE KB
# ============================================================

def update_knowledge_base():
    validate_card_kb()

    print("Loading existing knowledge base...")
    df = pd.read_csv(KB_PATH)

    original_count = len(df)

    print(f"Original articles: {original_count}")

    # Remove only articles belonging to the intents we are replacing.
    remaining = df[
        ~df["intent"].isin(CARD_INTENTS)
    ].copy()

    removed_count = original_count - len(remaining)

    print(
        f"Existing card articles removed: "
        f"{removed_count}"
    )

    card_df = pd.DataFrame(CARD_KB)

    updated = pd.concat(
        [remaining, card_df],
        ignore_index=True
    )

    updated = updated.drop_duplicates(
        subset=["kb_id"],
        keep="last"
    )

    updated = updated.sort_values(
        by=["category", "intent"]
    ).reset_index(drop=True)

    updated.to_csv(
        KB_PATH,
        index=False
    )

    print(
        f"Updated articles: {len(updated)}"
    )

    print(
        f"Updated card intents: "
        f"{len(card_df)}"
    )


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("SUPPORTAI CARD KB BUILDER")
    print("=" * 80)

    update_knowledge_base()

    print("\n" + "=" * 80)
    print("CARD KB UPDATE COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
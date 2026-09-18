from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "support_knowledge_base.csv"

START_KB_ID = 131


IDENTITY_KB = [
    {
        "category": "Account Management",
        "intent": "age_limit",
        "title": "Age requirements",
        "problem": "A customer wants to know the minimum age required to use the service.",
        "symptoms": "Minimum age; age requirement; how old do I need to be; age limit.",
        "resolution_steps": "1. Check the applicable age requirement.\n2. Confirm that the customer's age meets the requirement.\n3. If the customer does not meet the requirement, explain that the account cannot be opened or used under the applicable rules.",
        "additional_information": "Age requirements depend on the service and applicable account rules.",
        "escalation_condition": "Escalate if the customer's eligibility cannot be determined from the available age requirements.",
    },
    {
        "category": "Account Management",
        "intent": "edit_personal_details",
        "title": "Edit personal details",
        "problem": "A customer wants to change their personal account information.",
        "symptoms": "Change personal details; edit account information; update personal information; change profile details.",
        "resolution_steps": "1. Open the account or personal information settings.\n2. Select the detail that needs to be changed.\n3. Enter the updated information.\n4. Complete any verification required to save the change.",
        "additional_information": "Some personal information changes may require additional verification.",
        "escalation_condition": "Escalate if the customer cannot update their personal details through the available account settings or verification fails.",
    },
    {
        "category": "Account Security",
        "intent": "lost_or_stolen_phone",
        "title": "Lost or stolen phone",
        "problem": "A customer has lost their phone or believes their phone has been stolen.",
        "symptoms": "Lost phone; stolen phone; phone is missing; cannot access account because phone was lost.",
        "resolution_steps": "1. Secure access to the account as soon as possible.\n2. Use another trusted device or available recovery method if possible.\n3. Change relevant account credentials if account access may be compromised.\n4. Contact support if the customer cannot secure or recover the account.",
        "additional_information": "A lost or stolen phone can create a risk of unauthorised account access.",
        "escalation_condition": "Escalate if the customer cannot secure the account or suspects unauthorised access after losing the phone.",
    },
    {
        "category": "Login and Authentication",
        "intent": "passcode_forgotten",
        "title": "Forgotten passcode",
        "problem": "A customer has forgotten the passcode used to access the account.",
        "symptoms": "Forgot passcode; cannot remember passcode; unable to log in because of forgotten passcode.",
        "resolution_steps": "1. Use the available passcode recovery or reset option.\n2. Complete any identity or security verification requested.\n3. Set a new passcode when the recovery process is completed.\n4. Contact support if the recovery process cannot be completed.",
        "additional_information": "Passcode recovery may require additional account verification.",
        "escalation_condition": "Escalate if the customer cannot recover access through the available passcode recovery process.",
    },
    {
        "category": "Cards",
        "intent": "pin_blocked",
        "title": "Card PIN is blocked",
        "problem": "A customer's card PIN has been blocked.",
        "symptoms": "PIN blocked; PIN failed too many times; card PIN locked; cannot use PIN.",
        "resolution_steps": "1. Check the card and PIN status.\n2. Follow the available process to unblock or recover the PIN.\n3. Avoid repeated incorrect PIN attempts.\n4. Contact support if the PIN remains blocked.",
        "additional_information": "Repeated incorrect PIN attempts can result in the PIN being blocked.",
        "escalation_condition": "Escalate if the PIN cannot be unblocked through the available process or the card remains unusable.",
    },
    {
        "category": "Account Management",
        "intent": "terminate_account",
        "title": "Close an account",
        "problem": "A customer wants to permanently close their account.",
        "symptoms": "Delete account; close account; terminate account; stop using account permanently.",
        "resolution_steps": "1. Review the account closure requirements.\n2. Resolve any outstanding transactions or obligations before closure.\n3. Use the available account closure process.\n4. Contact support if the account cannot be closed through the normal process.",
        "additional_information": "Account closure may involve outstanding balances, transactions, or other account requirements.",
        "escalation_condition": "Escalate privacy, legal, unresolved dispute, or account closure requests that cannot be completed through the normal process.",
    },
    {
        "category": "Identity Verification",
        "intent": "unable_to_verify_identity",
        "title": "Unable to verify identity",
        "problem": "A customer cannot complete the identity verification process.",
        "symptoms": "Identity verification failed; cannot verify identity; verification does not work; unable to complete verification.",
        "resolution_steps": "1. Check that the submitted information and documents are correct.\n2. Follow the verification instructions carefully.\n3. Retry the verification process if permitted.\n4. Contact support if verification continues to fail.",
        "additional_information": "Identity verification may require accurate information and acceptable verification documents.",
        "escalation_condition": "Escalate if identity verification repeatedly fails or cannot be completed through the available process.",
    },
    {
        "category": "Identity Verification",
        "intent": "verify_my_identity",
        "title": "How to verify identity",
        "problem": "A customer wants to know how to complete identity verification.",
        "symptoms": "How do I verify my identity; identity verification process; verify account identity; what documents are needed for verification.",
        "resolution_steps": "1. Open the identity verification process.\n2. Provide the requested personal information and verification documents.\n3. Follow the verification instructions.\n4. Wait for the verification result or complete any additional requested step.",
        "additional_information": "Identity verification requirements depend on the account and applicable verification process.",
        "escalation_condition": "Escalate if the customer cannot complete the verification process or requires manual verification.",
    },
    {
        "category": "Identity Verification",
        "intent": "verify_source_of_funds",
        "title": "Verify source of funds",
        "problem": "A customer is asked to provide information verifying where their funds came from.",
        "symptoms": "Source of funds verification; verify where money came from; proof of source of funds; source of funds request.",
        "resolution_steps": "1. Review the source of funds information requested.\n2. Provide accurate supporting information or documents.\n3. Submit the requested information through the available verification process.\n4. Contact support if the source of funds verification cannot be completed.",
        "additional_information": "Source of funds checks may require supporting information or documents about the origin of funds.",
        "escalation_condition": "Escalate if the customer cannot complete the source of funds verification or requires manual review.",
    },
    {
        "category": "Identity Verification",
        "intent": "why_verify_identity",
        "title": "Why identity verification is required",
        "problem": "A customer wants to understand why identity verification is required.",
        "symptoms": "Why verify identity; why do I need identity verification; reason for identity check; why is verification required.",
        "resolution_steps": "1. Explain that identity verification is used to confirm the customer's identity.\n2. Explain that verification may be required before certain account functions can be used.\n3. Direct the customer to complete the verification process when required.",
        "additional_information": "Identity verification requirements depend on the account and applicable verification rules.",
        "escalation_condition": "Escalate if the customer has questions about a specific verification decision that cannot be resolved through the standard information.",
    },
]


def build():
    print("SUPPORTAI IDENTITY KB BUILDER")
    print("Loading existing knowledge base...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"Existing articles: {len(df)}")

    existing_intents = set(df["intent"].dropna().astype(str))

    new_rows = []
    next_id = START_KB_ID

    for article in IDENTITY_KB:
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
        print("No new identity articles to add.")
        return

    updated_df = pd.concat(
        [df, pd.DataFrame(new_rows)],
        ignore_index=True,
    )

    updated_df.to_csv(DATA_PATH, index=False)

    print(f"Identity articles added: {len(new_rows)}")
    print(f"Updated articles: {len(updated_df)}")
    print("IDENTITY KB UPDATE COMPLETED")


if __name__ == "__main__":
    build()
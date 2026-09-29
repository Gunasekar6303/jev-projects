import os
from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

load_dotenv()

# 1. Sample customer message
customer_message = (
    "I was charged twice for my subscription. "
    "Please refund the duplicate payment."
)


# 2. Send the message to JEV
with TypeSafeClient() as client:

    response = client.system_one(
        state={
            "customer_message": customer_message
        },
        questions={

            # Question 1: Identify the department
            "domain": Choice(
                instructions=(
                    "Which department should handle "
                    "this customer message?"
                ),
                criteria={
                    "billing": "Payments, invoices, subscriptions, refunds",
                    "technical": "Technical issues, bugs, troubleshooting",
                    "sales": "Product inquiries, pricing, purchases",
                    "other": "Anything outside the above departments",
                },
            ),

            # Question 2: Identify the customer's intent
            "intent": Choice(
                instructions=(
                    "What is the primary intent of "
                    "the customer's message?"
                ),
                criteria={
                    "refund_request": "Requests a refund",
                    "payment_issue": "Reports a payment or billing problem",
                    "technical_support": "Requests technical assistance",
                    "product_inquiry": "Asks about a product or service",
                    "other": "Intent does not match the other options",
                },
            ),
        },
    )


# 3. Read the structured answers
domain_answer = response.choices["domain"]
intent_answer = response.choices["intent"]


# 4. Display the results
print("\n--- JEV CUSTOMER TRIAGE ---")

print("Customer message:", customer_message)

print("\nDomain:", domain_answer.choice)
print("Domain confidence:", domain_answer.confidence)

print("\nIntent:", intent_answer.choice)
print("Intent confidence:", intent_answer.confidence)
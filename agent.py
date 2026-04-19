# agent.py
from groq import Groq
from dotenv import load_dotenv
import os
from memory import save_memory, get_memory
from actions import send_payment_link, schedule_callback, create_ticket, offer_emi

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a collections and service resolution assistant for a telecom company.
Your job is to:
1. Understand the customer's issue.
2. Be polite and empathetic.
3. Offer EMI if amount is more than ₹5000.
4. Escalate to human agent if customer is very angry.
5. Always offer a solution.
"""

def run_agent(customer_id, user_message):
    # Get past history for this customer
    history = get_memory(customer_id)

    full_prompt = f"""
Customer ID: {customer_id}
Past History: {history}
Customer says: {user_message}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ]
    )
    reply = response.choices[0].message.content

    # Save this interaction to memory
    save_memory(customer_id, f"Customer said: {user_message} | Agent replied: {reply[:60]}")

    return reply
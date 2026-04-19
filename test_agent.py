from agent import run_agent
from actions import send_payment_link, offer_emi, schedule_callback
from memory import get_memory
customer_id = "CUST_001"

while True:
    user_input = input("Customer: ")
    if user_input.lower() == "exit":
        break

    if user_input.lower() == "history":
        print(f"\n📋 Memory for {customer_id}:")
        print(get_memory(customer_id))
        print()
        continue

    reply = run_agent(customer_id, user_input)
    print(f"Agent: {reply}")
    print()

    # Simple keyword-based action triggers
    if "payment" in user_input.lower():
        print(send_payment_link(customer_id, 2500))
    elif "emi" in user_input.lower():
        print(offer_emi(customer_id, 6000))
    elif "callback" in user_input.lower():
        print(schedule_callback(customer_id, "Tomorrow 10 AM"))

# actions.py
# Functions the agent can call to take real-world actions

def send_payment_link(customer_id, amount):
    # Later: connect to Razorpay / Paytm API
    print(f"[Action] Payment link sent to {customer_id} for ₹{amount}")
    return f"Payment link of ₹{amount} has been sent to customer {customer_id}."

def schedule_callback(customer_id, time_slot):
    # Later: connect to CRM or calendar API
    print(f"[Action] Callback scheduled for {customer_id} at {time_slot}")
    return f"Callback scheduled for customer {customer_id} at {time_slot}."

def create_ticket(customer_id, issue):
    # Later: connect to Zendesk / Freshdesk
    print(f"[Action] Ticket created for {customer_id}: {issue}")
    return f"Support ticket created for {customer_id} regarding: {issue}."

def offer_emi(customer_id, amount):
    emi = round(amount / 3, 2)
    print(f"[Action] EMI offered to {customer_id}: ₹{emi}/month for 3 months")
    return f"EMI plan offered: ₹{emi}/month for 3 months for customer {customer_id}."
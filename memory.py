# Stores and retrieves customer interaction history
# Uses a JSON file so memory PERSISTS even after restarting the program

import json
import os

MEMORY_FILE = "memory_store.json"  

# ─────────────────────────────────────────────
# LOAD all data from the JSON file
# ─────────────────────────────────────────────
def load_all():
    if not os.path.exists(MEMORY_FILE):
        return {}   
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)  

# ─────────────────────────────────────────────
# SAVE all data back to the JSON file
# ─────────────────────────────────────────────
def save_all(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)   

# ─────────────────────────────────────────────
# SAVE one interaction for a customer
# ─────────────────────────────────────────────
def save_memory(customer_id, note):
    data = load_all()                      # read existing data
    if customer_id not in data:
        data[customer_id] = []             # create empty list for new customer
    data[customer_id].append(note)         # add new note to the list
    save_all(data)                         # save back to file
    print(f"[Memory saved for {customer_id}]")

# ─────────────────────────────────────────────
# GET full history for a customer
# ─────────────────────────────────────────────
def get_memory(customer_id):
    data = load_all()
    history = data.get(customer_id, [])    # get list, return [] if not found
    if not history:
        return "No previous history found."
    return " | ".join(history)             # join all notes into one string

# ─────────────────────────────────────────────
# DELETE history for a customer (optional)
# ─────────────────────────────────────────────
def clear_memory(customer_id):
    data = load_all()
    if customer_id in data:
        del data[customer_id]
        save_all(data)
        print(f"[Memory cleared for {customer_id}]")

# ─────────────────────────────────────────────
# VIEW all customers stored (for testing)
# ─────────────────────────────────────────────
def show_all_customers():
    data = load_all()
    if not data:
        print("No memory stored yet.")
        return
    print("\n📋 All stored customer memory:")
    for customer_id, notes in data.items():
        print(f"\n  Customer: {customer_id}")
        for i, note in enumerate(notes, 1):
            print(f"    {i}. {note}")

# ─────────────────────────────────────────────
# TEST: run this file directly to check memory
# python memory.py
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing memory module...")

    save_memory("CUST_001", "Customer said: I can't pay | Agent: offered EMI plan")
    save_memory("CUST_001", "Customer said: what is EMI | Agent: explained Rs.2000/month for 3 months")
    save_memory("CUST_002", "Customer said: send payment link | Agent: link sent for Rs.2500")

    print("\nMemory for CUST_001:")
    print(get_memory("CUST_001"))

    print("\nMemory for CUST_002:")
    print(get_memory("CUST_002"))

    show_all_customers()
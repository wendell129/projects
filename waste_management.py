import json
import os

# File paths
USER_DATA_FILE = "users.json"
TRANSACTION_DATA_FILE = "transactions.json"

# Waste rates per kilogram
WASTE_RATES = {
    "plastic bottle": 10,
    "metal can": 25,
    "glass bottle": 15,
    "paper": 10,
    "electronic waste": 120
}


def initialize_files():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({"last_id": 0, "users": {}}, f)
    if not os.path.exists(TRANSACTION_DATA_FILE):
        with open(TRANSACTION_DATA_FILE, 'w') as f:
            json.dump({}, f)


def generate_customer_id():
    with open(USER_DATA_FILE, 'r+') as f:
        data = json.load(f)
        last_id = data.get("last_id", 0)

        if last_id >= 999:
            print("Maximum number of users reached.")
            return None

        new_id = last_id + 1
        data["last_id"] = new_id
        f.seek(0)
        json.dump(data, f)

    return f"{new_id:03}"


def register_user(username):
    with open(USER_DATA_FILE, 'r+') as f:
        data = json.load(f)
        users = data.get("users", {})

        if username in users:
            print("Username already exists. Please choose another one.")
            return None

        # Generate a new customer ID
        customer_id = generate_customer_id()
        if not customer_id:
            return None

        users[username] = {"customer_id": customer_id, "balance": 0}
        data["users"] = users

        f.seek(0)
        json.dump(data, f)

    print(f"User '{username}' registered successfully with Customer ID: {customer_id}!")
    return username


def login_user(username):
    with open(USER_DATA_FILE, 'r') as f:
        data = json.load(f)
        users = data.get("users", {})

        if username in users:
            customer_id = users[username]["customer_id"]
            print(f"Welcome back, {username}! Your Customer ID is {customer_id}.")
            return True
        else:
            print("Username not found. Please register first.")
            return False


def record_waste(username, waste_type, weight_kg):
    if waste_type not in WASTE_RATES:
        print("Invalid waste type. Options: plastic bottle, metal can, glass bottle, paper, electronic waste.")
        return

    reward = WASTE_RATES[waste_type] * weight_kg

    # Update user balance
    with open(USER_DATA_FILE, 'r+') as f:
        data = json.load(f)
        users = data.get("users", {})
        users[username]["balance"] += reward
        data["users"] = users

        f.seek(0)
        json.dump(data, f)

    # Log transaction
    transaction = {
        "waste_type": waste_type,
        "weight_kg": weight_kg,
        "reward": reward
    }
    with open(TRANSACTION_DATA_FILE, 'r+') as f:
        transactions = json.load(f)
        transactions.setdefault(username, []).append(transaction)

        f.seek(0)
        json.dump(transactions, f)

    # Calculate total weight of all waste types for the user
    total_weight = sum(t["weight_kg"] for t in transactions[username])

    print(f"Recorded {weight_kg} kg of {waste_type}. You earned {reward} pesos.")
    print(f"Total waste recorded by {username}: {total_weight} kg.")


def view_user_data(username):
    with open(USER_DATA_FILE, 'r') as f:
        data = json.load(f)
        users = data.get("users", {})
        user_info = users.get(username, {})

        balance = user_info.get("balance", 0)
        customer_id = user_info.get("customer_id", "N/A")
        print(f"Customer ID: {customer_id}")
        print(f"Total balance for {username}: {balance} pesos")

    with open(TRANSACTION_DATA_FILE, 'r') as f:
        transactions = json.load(f)
        user_transactions = transactions.get(username, [])

        if user_transactions:
            print("\nTransaction History:")
            for t in user_transactions:
                print(f"{t['weight_kg']} kg of {t['waste_type']} - Earned {t['reward']} pesos")
        else:
            print("No transactions recorded.")

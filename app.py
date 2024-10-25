# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Function to calculate the total balance
def total_balance():
    return sum(transaction['amount'] for transaction in transactions)

#login

# Default credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password"

@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # Here you would check the credentials (e.g., against a database)
        if username == "admin" and password == "password":  # Replace with actual validation
            return redirect(url_for("get_transactions"))  # Redirect to the main page or dashboard
        else:
            return "Invalid username or password", 401

    return render_template("login.html")


# Route to display all transactions and total balance
@app.route("/")
def get_transactions():
    balance = total_balance()  # Calculate the balance
    return render_template("transactions.html", transactions=transactions, balance=balance)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Search transactions within an amount range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        try:
            # Retrieve minimum and maximum amount from the form
            min_amount = float(request.form.get("min_amount"))
            max_amount = float(request.form.get("max_amount"))

            # Filter transactions based on the specified range
            filtered_transactions = [
                transaction for transaction in transactions
                if min_amount <= transaction["amount"] <= max_amount
            ]

            # Pass filtered transactions to the template
            return render_template("transactions.html", transactions=filtered_transactions, balance=total_balance())

        except (ValueError, TypeError):
            return render_template("search.html", error="Please enter valid numbers for the amount range.")

    # Render the search form if GET request
    return render_template("search.html")
    
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

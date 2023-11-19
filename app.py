# Import libraries
from flask import Flask, request, url_for, redirect, render_template


# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route('/add', methods = ['GET', 'POST'])
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

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
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

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
            if transaction['id'] == transaction_id:
                transactions.remove(transaction)
                break
    return redirect(url_for("get_transactions"))

# Search transactions
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form.get('min_amount'))
        max_amount = float(request.form.get('max_amount'))
        filtered_transactions = [trans for trans in transactions if min_amount <= trans['amount'] <= max_amount]
        return render_template('transactions.html', transactions=filtered_transactions)
    else:
        return render_template('search.html')

# Total balance
@app.route('/balance')
def total_balance():
    total_balance = sum(trans['amount'] for trans in transactions)
    return render_template('transactions.html', transactions=transactions, total_balance=total_balance)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
'''Main app routes'''
from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)
# Sample data

transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    '''render all transactions'''
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    '''Process GET and POST requests for adding a new transaction'''
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for('get_transactions'))

    return render_template('form.html')

# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    '''Update a transaction and redirect to transaction list'''
    if request.method == 'POST':
        for transaction in transactions:
            if transaction_id == transaction['id']:
                transaction['date'] = request.form['date']
                transaction['amount'] = float(request.form['amount'])

        return redirect(url_for('get_transactions'))

    for transaction in transactions:
        if transaction_id == transaction['id']:
            return render_template('edit.html', transaction=transaction)

    return {'message:' f'{transaction_id} not found'}, 404
# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    '''DELETE transaction by id'''
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for('get_transactions'))

@app.route('/search', methods=['GET', 'POST'])
def search_transactions ():
    '''Search transactions'''
    if request.method == 'POST':
        min_amt = float(request.form['min_amount'])
        max_amt = float(request.form['max_amount'])
        found_transactions = []

        for transaction in transactions:
            if transaction['amount'] >= min_amt and (transaction['amount'] <= max_amt):
                found_transactions.append(transaction)

        return render_template('transactions.html', transactions=found_transactions)

    return render_template('search.html')

@app.route('/balance')
def total_balance():
    '''Total balance of all transactions'''
    total = 0
    for transaction in transactions:
        total += transaction['amount']

    final_total = f'Total : {str(total)}'
    return render_template('transactions.html', transactions=transactions, total=final_total)
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

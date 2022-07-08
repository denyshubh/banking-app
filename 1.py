import psycopg
from flask import Flask, request
from datetime import date
app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Welcome to Banking Application'


@app.route('/customers', methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        data = request.get_json()  # reading data sent from postman
        res = insert_customers(data)
        return res
    elif request.method == "GET":
        res = get_customers()
        return res


@app.route('/customers/<string:customer_id>', methods=["GET", "PUT", "DELETE"])
def customer(customer_id):
    if request.method == "GET":
        res = get_customer(customer_id)
        return res
    elif request.method == "PUT":
        data = request.get_json()
        res = update_customer(customer_id, data)
        return res
    elif request.method == "DELETE":
        res = delete_customer(customer_id)
        return res


@app.route('/customers/<string:customer_id>/accounts', methods=["POST", "GET"])
def customer_accounts(customer_id):
    if request.method == "POST":
        data = request.get_json()
        res = insert_accounts(customer_id, data)
        return res
    elif request.method == "GET":
        # GET / customer / {customer_id} / accounts?amountLessThan = 1000 & amountGreaterThan = 300:
        # Get all accounts for customer id of X with balances between Y and Z ( if customer exists)
        amountLessThan = request.args.get("amountLessThan") or 2147483647
        amountGreaterThan = request.args.get("amountGreaterThan") or -2147483648
        res = get_customer_account(customer_id, amountGreaterThan, amountLessThan)
        return res


@app.route('/customers/<string:customer_id>/accounts/<string:account_id>', methods=["GET", "PUT", "DELETE"])
def customer_account(customer_id, account_id):
    if request.method == "GET":
        res = get_account(account_id)
        return res
    elif request.method == "PUT":
        data = request.get_json()
        res = update_account(account_id, data)
        return res
    elif request.method == "DELETE":
        res = delete_account(account_id)
        return res


@app.route('/accounts')
def accounts():
    amountLessThan = request.args.get("amountLessThan") or 2147483647
    amountGreaterThan = request.args.get("amountGreaterThan") or -2147483648
    return get_accounts(amountGreaterThan, amountLessThan)

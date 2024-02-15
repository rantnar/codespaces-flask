from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/add_invoice", methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'POST':
        invoice_data = {
            'invoice_number': request.form.get('invoice_number'),
            'invoice_quote': request.form.get('invoice_quote'),
            'invoice_date_issue': request.form.get('invoice_date_issue'),
            'currency': request.form.get('currency'),
            'status': False,
            'payments': []
        }
        os.makedirs('data/invoices/singles', exist_ok=True)
        with open(f'data/invoices/singles/{invoice_data["invoice_number"]}.json', 'w') as f:
            json.dump(invoice_data, f)
        return 'Invoice added'
    return render_template("add_invoice.html")

@app.route("/invoices", methods=['GET'])
def invoices():
    invoice_number = request.args.get('invoice_number')
    invoices = []
    for filename in os.listdir('data/invoices/singles'):
        with open(f'data/invoices/singles/{filename}') as f:
            invoice = json.load(f)
            if invoice_number is None or invoice['invoice_number'] == invoice_number:
                invoices.append(invoice)
    return render_template("invoices.html", invoices=invoices)

@app.route("/add_payment", methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        invoice_number = request.form.get('invoice_number')
        payment_amount = request.form.get('payment_amount')
        payment_date = request.form.get('payment_date')
        with open(f'data/invoices/singles/{invoice_number}.json', 'r+') as f:
            invoice = json.load(f)
            payment = {
                'amount': payment_amount,
                'date': payment_date
            }
            invoice['payments'].append(payment)
            f.seek(0)
            json.dump(invoice, f)
            f.truncate()
        return 'Payment added'
    else:
        invoice_number = request.args.get('invoice_number')
        invoices = []
        for filename in os.listdir('data/invoices/singles'):
            with open(f'data/invoices/singles/{filename}') as f:
                invoice = json.load(f)
                if invoice['status'] == False and (invoice_number is None or invoice['invoice_number'] == invoice_number):
                    invoices.append(invoice)
        return render_template("add_payment.html", invoices=invoices)


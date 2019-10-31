from flask import Flask, request, jsonify
import requests
import json
from os.path import join
import os

# Init app
app = Flask(__name__)

url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com"
headers = {
    'identity': 'Group4',
    'token': 'e908711e-8acc-4a4a-b273-9e33395b4cd2'
}

@app.route('/<userName>', methods=['GET'])
def get_customer(userName):
    x = Customer(userName).toJSON()
    cust = {userName:x}
    return cust

class Customer():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)

    def __init__(self, username):
        self.username = username
        #print(self.username)
        self.customerid = int(self.get_customerid()['customerId'])
        #print(self.customerid)
        self.account_number = self.dept_account()
        #print("ACCT")
        #print(self.account_number)
        self.credit_number = self.credit_acct()
        #print("CREDIT")
        #print(self.credit_number)
        self.acc_bal = self.get_account()
        #print("ACT BAL")
        #print(self.acc_bal)
        self.credit = self.get_credit()
        #print("CREDIT BAL")
        #print(self.credit)
        self.message = self.personal_msg()
        #print("MESSAGES")
        #print(self.message)

    # getting back customerid
    def get_customerid(self):
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/{}".format(self.username), headers=headers).json()
        return response

    # getting back the username
    def get_username(self):
        return self.username

    # get deposit account
    def dept_account(self):
        response = requests.get(
            "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{}".format(
                self.customerid),
            headers=headers)
        account = []
        for i in response.json():
            account.append(i['accountId'])
        return account

    # get customer details
    def get_customerdet(self):
        response = requests.get(
            join("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/{}".format(self.customerid),
                 "/details"), headers=headers).json()
        return response

    # get credit account
    def credit_acct(self):
        response = requests.get(
            "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/credit/{}".format(
                self.customerid),
            headers=headers).json()
        account = []
        for i in response:
            account.append(i['accountId'])
        return account

    # get personal messages
    def personal_msg(self):
        response = requests.get(
            "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/message/{}".format(self.customerid),
            headers=headers).json()
        for i in response:
            del i['messageId']
        return response

    #returning dictionary of key: accountid value: balance
    def get_account(self):
        acc_bal_dict = {}
        for i in self.account_number:
            x = Account(i)
            acc_bal_dict[str(i)] = x.balance
        return acc_bal_dict

    #returning dictionary of key: creditaccountid value: outstanding amt
    def get_credit(self):
        credit_dict = {}
        for i in self.credit_number:
            x = CreditAccount(i)
            credit_dict[str(i)] = x.outstanding_amount
        return credit_dict



class Account():
    def __init__(self, account_id):
        """Account Object
        -----------------------
        Input string: account_id, string: account_type, string: account_number"""
        self.account_id = account_id
        self.balance_json = self.get_balance()
        self.transactions_data = self.get_transaction('01-01-2018', '01-31-2019')
        self.displayName = self.balance_json['displayName']
        self.account_type = self.balance_json['accountType']
        self.account_number = self.balance_json['accountNumber']
        self.balance = self.balance_json['availableBalance']
        self.credit = self.get_trans_sum('CREDIT')
        self.debit = self.get_trans_sum("DEBIT")

    def get_transaction(self, from_date, to_date):
        '''method to return list of dictionary of transaction
         input from_date and to_date-> format = dd-mm-yyyy'''

        params = {'from':from_date, "to":to_date}
        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/{}".format(self.account_id),
                                headers=headers, params=params)
        transactions = []
        for i in response.json():
            transactions.append(i)
        return transactions

    def get_balance(self, month=False, year=False):
        '''Return balance of account. If no month or year: Return latest balance
        month: 'mm', year: 'yyyy' '''
        if month == False or year == False:
            'Check for latest balance by setting params null'
            params=False
        else:
            params = {'month': month, 'year': year}

        response = requests.get("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{0}/balance".format(self.account_id),
                                headers = headers, params=params)
        #print(response.status_code)
        #print(response.json())
        return response.json()

    def get_trans_sum(self, type):
        '''Get transaction detail based on required data
        type: Either "DEBIT" -> Returns debit level in account| or "CREDIT"-> Return total credit level in account '''
        sum = 0
        for i in self.transactions_data:
            if i['type'] == type:
                sum += float(i['amount'])

        if type =='DEBIT':
            return round(sum, 2)
        else:
            return -round(sum, 2)

class CreditAccount():
    def __init__(self, account_id):
        '''Credit'''
        self.account_id = account_id
        self.json = self.get_outstanding_amount()
        self.outstanding_amount = self.json['outstandingAmount']
        self.date_payable = self.json['datePayable']
        self.currency = self.json['currency']
        self.displayName = self.json['displayName']
        self.card_number = self.json['cardNumber']

    def get_outstanding_amount(self):
        response = requests.get(
            "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/credit/{0}/balance".format(
                self.account_id),
            headers=headers)
        return response.json()
# response = requests.get(join("http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/2",
#                                     "details"), headers=headers).json()
# print(response['firstName'])

#response = requests.get(
#    "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/credit/2",
#    headers=headers)
#print(response.json())
# Run Server
if __name__ == '__main__':
    app.run(debug=True)

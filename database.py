from flask import Flask, request, jsonify
import requests
from os.path import join
url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com"
headers = {'identity': 'Group4',
           'token': 'e908711e-8acc-4a4a-b273-9e33395b4cd2',}

class Customer():
    def __init__(self, username, customerid, name, account, gender, firstname, lastname, lastlogin, dob):
        self.username = username
        self.customerid = customerid
        self.name = name
        self.account = account
        self.gender = gender
        self.firstname = firstname
        self.lastname = lastname
        self.lastlogin = lastlogin
        self.dob = dob

    def get_name(self):
        return self.name

    def get_account(self):
        return self.account


class Account():
    def __init__(self, account_id):
        '''Account Object
        -----------------------
        Input string: account_id, string: account_type, string: account_number'''
        self.account_id = account_id
        self.balance_json = self.get_balance()
        self.transactions = self.get_transaction('01-01-2018', '02-01-2019')
        self.displayName = self.balance_json['displayName']
        self.account_type = self.balance_json['accountType']
        self.account_number = self.balance_json['accountNumber']
        self.balance = self.balance_json['availableBalance']

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

    def get_balance(self, month = False, year = False):
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

if __name__ == '__main__':
    y  =Account(74)
    print('-----Account transactions:-------\n ', y.transactions)
    x = CreditAccount(106)
    print(x.currency)
    print(x.outstanding_amount)
    #print("Current balance: ", x.balance)
    #print("Account type:", x.account_type)
    #print("display name: ", x.displayName)

    #x.get_transaction('01-01-2018', '01-31-2018')
    #print(x.get_balance('01', '2018'))

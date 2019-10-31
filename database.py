from flask import Flask, request, jsonify
import requests
from os.path import join
url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com"
headers = {'identity': 'Group4',
           'token': 'e908711e-8acc-4a4a-b273-9e33395b4cd2',}

class Customer():
    def __init__(self, username, customerid):
        self.username = username
        self.customerid = customerid
        self.account_number = self.dept_account()
        self.account = self.get_account()
        self.credit_number = self.credit_acct()
        self.credit = self.get_credit()
        self.total_transaction = self.get_transaction()

    def get_customerid(self):
        return self.customerid

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
        response = request.get(
            "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/message/{}".format(self.customerid),
            headers=headers).json()
        return response

    # getting account no with the balance
    def get_account(self):
        acc_bal_dict = {}
        for i in self.account_number:
            x = Account(i)
            acc_bal_dict[str(i)] = x
        print("accountbalance")
        print(acc_bal_dict)
        return acc_bal_dict

    def get_credit(self):
        credit_dict = {}
        for i in self.credit_number:
            x = CreditAccount(i)
            credit_dict[str(i)] = x
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

if __name__ == '__main__':
    x = Account(10)
    print(x.displayName)
    print(x.balance)
    print(x.debit)
    print(x.credit)
    #print("Current balance: ", x.balance)
    #print("Account type:", x.account_type)
    #print("display name: ", x.displayName)

    #x.get_transaction('01-01-2018', '01-31-2018')
    #print(x.get_balance('01', '2018'))


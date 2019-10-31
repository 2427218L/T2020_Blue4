class Customer():
    def __init__(self, username, customerid):
        self.username = username
        #print(self.username)
        self.customerid = customerid
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
        return self.customerid

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

from services.TransactionService import TransactionService

class TransactionController:


    __transactionService = TransactionService()


    # return -1 if account doesn't exist
    # 0 if account is None
    # account itself
    def getAccountById(self, id):

        account = self.__transactionService.getAccountById(id)

        if(account == None):
            return 0
        return round(account, 2)


    # return False if account doesn't exist
    # True if everything is fine
    def addMoneyToAccountById(self, id, money):

        money = round(money, 2)
        currentAccount = self.getAccountById(id)

        if(currentAccount != -1):
            self.__transactionService.updateAccountById(id, currentAccount + money)
            return True
        return False
    

    # return -1 if account doesn't exist
    # -2 if user don't have money on Account
    # 0 if everything is fine
    def takeOffMoneyFromAccountById(self, id, money):
        
        money = round(money, 2)
        currentAccount = self.getAccountById(id)

        if(currentAccount == -1):
            return -1

        if(money > currentAccount):
            return -2
        
        self.__transactionService.updateAccountById(id, currentAccount - money)
        return 0
    

    # return -1 if account From doesn't exist
    # -2 if user don't have money for transfering
    # -3 if account To doesn't exist
    # 0 if everything is fine
    def addMoneyFromAccountToAnotherAccount(self, from_id, to_id, money):

        money = round(money, 2)

        statusTakeOffMoney = self.takeOffMoneyFromAccountById(from_id, money)

        if(statusTakeOffMoney == -1 or statusTakeOffMoney == -2):
            return statusTakeOffMoney
        
        if(self.addMoneyToAccountById(to_id, money) == True):
            return 0
        else:
            self.addMoneyToAccountById(from_id, money)
            return -3



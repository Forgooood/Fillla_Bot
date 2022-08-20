from controllers.UserController import UserController

class TransactionService:
    
    __userController = UserController()


    def getAccountById(self, id):
        if(self.__userController.checkIfUserExistInDBById(id) == True):
            return self.__userController.getUserMoneyById(id)
        return -1
    
    
    def updateAccountById(self, id, account):
        self.__userController.updateUserMoneyById(id, account)

        


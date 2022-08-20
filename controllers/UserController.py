from services.UserService import UserService

class UserController:

    __userService = UserService()


    def createUserIfNotExist(self, id, name):
        self.__userService.insertData(id, "name", name)
    
    
    def checkIfUserExistInDBById(self, id):
        return self.__userService.checkIfUserExistInDB(id)


    def getUserById(self, id):
        return self.__userService.getUserById(id)

    
    # return False if user not found
    # return True if user deleted
    def deleteUserById(self, id):
        if(self.checkIfUserExistInDBById(id) == True):
            self.deleteUserById(id)
            return True
        return False


    def getUserNameById(self, id):
        return self.__userService.getDataById(id, "name")


    def getUserDescriptionById(self, id):
        return self.__userService.getDataById(id, "description")


    def getUserSexById(self, id):
        return self.__userService.getDataById(id, "sex")

    
    def getUserMoneyById(self, id):
        return self.__userService.getDataById(id, "money")


    def getUserMaritalStatusById(self, id):
        return self.__userService.getDataById(id, "marital_status")


    def getUserJobById(self, id):
        return self.__userService.getDataById(id, "job")


    def getUserAgeById(self, id):
        return self.__userService.getDataById(id, "age")

    
    def getUserCupboardById(self, id):
        return self.__userService.getDataById(id, "cupboard")


    def getUserStolenByById(self, id):
        return self.__userService.getDataById(id, "stolen_by")


    def getUserLastCallById(self, id):
        return self.__userService.getDataById(id, "lastcall")


    def updateUserNameById(self, id, name):
        self.__userService.updateDataById(id, "name", name)


    def updateUserDescriptionById(self, id, description):
        self.__userService.updateDataById(id, "description", description)


    def updatetUserSexById(self, id, sex):
        self.__userService.updateDataById(id, "sex", sex)

    
    def updateUserMoneyById(self, id, money):
        self.__userService.updateDataById(id, "money", money)


    def updateUserMaritalStatusById(self, id, maritalStatus):
        self.__userService.updateDataById(id, "marital_status", maritalStatus)


    def updateUserJobById(self, id, job):
        self.__userService.updateDataById(id, "job", job)


    def updateUserAgeById(self, id, age):
        self.__userService.updateDataById(id, "age", age)

    
    def updateUserCupboardById(self, id, cupboard):
        self.__userService.updateDataById(id, "cupboard", cupboard)


    def updateUserStolenByById(self, id, stolenBy):
        self.__userService.updateDataById(id, "stolen_by", stolenBy)


    def updateUserLastcallById(self, id, lastcall):
        self.__userService.updateDataById(id, "lastcall", lastcall)
    



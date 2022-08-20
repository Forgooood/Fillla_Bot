from controllers.UserController import UserController

class CupboardService:

    __userController = UserController()


    def checkIfUserHaveCupboardById(self, id):
        cupboard = self.__userController.getUserCupboardById(id)
        if(cupboard == None):
            return False
        return True



    def getUsersFromCupboardById(self, id):
        if(self.checkIfUserHaveCupboardById(id) == False):
            return None
        
        cupboard = self.__userController.getUserCupboardById(id)     
        textCup = cupboard.split(":") # get cupboard in fornmat: ["Детский", "12312323232,123223213"]

        if(len(textCup) == 1):
            return None
        
        return textCup[1].split(',')



    def getTypeCupboard(self, id):
        if(self.checkIfUserHaveCupboardById(id) == False):
            return None
        cupboard = self.__userController.getUserCupboardById(id)     
        textCup = cupboard.split(":")
        return textCup[0]


    
    # 0 if user added to cupboard
    # -1 if owner don't have cupboard
    # -2 if owner and the user is one person
    # -3 if the user was stolen
    def addUserInCupboardById(self, ownerKupboardId, userId):

        if(self.checkIfUserHaveCupboardById(ownerKupboardId) == False):
            return -1

        if(ownerKupboardId == userId):
            return -2
        
        if(self.__userController.getUserStolenByById(userId) != None):
            return -3

        cupboard = self.__userController.getUserCupboardById(ownerKupboardId)     
        textCup = cupboard.split(":") # get cupboard in fornmat: ["Детский", "12312323232,123223213"]

        if(len(textCup) == 1):
            cupboard = cupboard + ":" + str(userId)
        else:
            cupboard = cupboard + "," + str(userId)
        
        self.__userController.updateUserCupboardById(ownerKupboardId, cupboard)
        self.__userController.updateUserStolenByById(userId, ownerKupboardId)
        return 0    


    # 0 if user deleted
    # -1 if owner don't have cupboard
    # -2 if owner and the user is one person
    # -3 if owner did't steal anyone 
    # -4 if cupboard's owner didn't steal the user 
    def deleteUserFromCupboardById(self, ownerKupboardId, userId):

        if(self.checkIfUserHaveCupboardById(ownerKupboardId) == False):
            return -1
        
        if(ownerKupboardId == userId):
            return -2

        usersArr = self.getUsersFromCupboardById(ownerKupboardId)

        if(usersArr == None):
            return -3

        if(str(userId) not in usersArr):
            return -4
        
        typeCup = self.getTypeCupboard(ownerKupboardId)

        if(len(usersArr) == 1):
            self.__userController.updateUserCupboardById(ownerKupboardId, typeCup)
            self.__userController.updateUserStolenByById(userId, None)
            return 0

        typeCup = typeCup + ":"
        usersArr.remove(str(userId))

        i = 0
        while(i < len(usersArr)):
            typeCup = typeCup + usersArr[i]

            if(i != len(usersArr) - 1):
                typeCup = typeCup + ','

            i = i + 1
        
        self.__userController.updateUserCupboardById(ownerKupboardId, typeCup)
        self.__userController.updateUserStolenByById(userId, None)
        return 0


    
    # 0 if cupboard is empty
    # -1 if user don't have cupboard
    # -2 if user did't steal anyone 
    def deleteAllUsersFromCupboardById(self, id):

        if(self.checkIfUserHaveCupboardById(id) == False):
            return -1

        typeCup = self.getTypeCupboard(id)
        users = self.getUsersFromCupboardById(id)
        if(users == None):
            return -2

        for user in users:
            self.__userController.updateUserStolenByById(int(user), None)

        self.__userController.updateUserCupboardById(id, typeCup)
        return 0



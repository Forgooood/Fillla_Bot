from services.CupboardService import CupboardService
from services.UserService import UserService

class CupboardController:

    __cupboardService = CupboardService()
    __userService = UserService()



    # 0 if hider stole hiden
    # -1 if hider don't have cupboard
    # -2 if hider and the hiden is one person
    # -3 if the hiden is already stolen
    def hideUserInCupboard(self, hiderId, hidenId):
        return self.__cupboardService.addUserInCupboardById(hiderId, hidenId)



    def getCupboardTypeById(self, id):
        return self.__cupboardService.getTypeCupboard(id)



    def checkIfUserHaveCupboard(self, id):
        return self.__cupboardService.checkIfUserHaveCupboardById(id)



    def getUsersFromCupboardById(self, id):
        return self.__cupboardService.getUsersFromCupboardById(id)



    def checkIfCupboardIsEmptyById(self, id):
        if(self.checkIfUserHaveCupboard(id) == True):
            if(self.__cupboardService.getUsersFromCupboardById(id) != None):
                return True
        return False

       
        
    # None if user don't have cupboard
    def getInfoAboutCupboardById(self, id):
        return self.__userService.getCupboardById(id)
    


    # 0 if user deleted
    # -1 if owner don't have cupboard
    # -2 if owner and the user is one person
    # -3 if owner did't steal anyone 
    # -4 if cupboard's owner didn't steal the user
    def expelUserFromKupboardById(self, ownerCupboardId, expeledUserId):
        return self.__cupboardService.deleteUserFromCupboardById(ownerCupboardId, expeledUserId)
    


    # 0 if cupboard is empty
    # -1 if user don't have cupboard
    # -2 if user did't steal anyone 
    def freeCupboardById(self, id):
        return self.__cupboardService.deleteAllUsersFromCupboardById(id)

        





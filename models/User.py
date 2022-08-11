class User:

    def __init__(self, id, name, description, sex, money, marital_status, job):
        self.__id = id
        self.__name = name
        self.__description = description
        self.__sex = sex
        self.__money = money
        self.__marital_status = marital_status
        self.__job = job
    

    def getId(self):
        return self.__id


    def getName(self):
        return self.__name


    def getDescription(self):
        return self.__description


    def getSex(self):
        return self.__sex


    def getMoney(self):
        return self.__money


    def getMaritalStatus(self):
        return self.__marital_status


    def getJob(self):
        return self.__job
    
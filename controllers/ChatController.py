import secrets
import time

from controllers.UserController import UserController
from controllers.TransactionController import TransactionController
from controllers.KeyboardController import KeyboardController
from controllers.CupboardController import CupboardController

from exeptions.ExeptionHandler import ExeptionHandler

from resources.Resources import Resources


class ChatController:
    

    __keyboardController = KeyboardController()
    __userController = UserController()
    __transactionController = TransactionController()
    __cupboardController = CupboardController()
    __exeptionHandler = ExeptionHandler()



    def __init__(self, bot):
        self.__bot = bot



    def getUserLink(self, userId, coveredTextForLink):
        return "["+ coveredTextForLink +"](tg://user?id=" + str(userId) + ")"



    def getTrueWithLuck(self, persent):
        
        persent = persent * 10
        if(persent < 1):
            print("Error: person should be more than 0.1")
            return False

        if(secrets.randbelow(999) < persent):
            return True
        
        return False



    def sendSmart(self, message, text, keyboard):

        if (message.chat.id < 0):
            self.__bot.send_message(message.chat.id, text, parse_mode="Markdown")
        else:
            self.__bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode="Markdown")



    def replySmart(self, message, text, keyboard):

        if (message.chat.id < 0):
            self.__bot.reply_to(message, text, parse_mode="Markdown")
        else:
            self.__bot.reply_to(message, text, reply_markup=keyboard, parse_mode="Markdown")    



    def checkChatIsPrivate(self, message):

        if(message.chat.id < 0):
            self.__bot.reply_to(message, "Введите эту команду в чате со мной, пожалуйста.", reply_markup=self.__keyboardController.goToBotKeyboard())
            return False
        return True



    def takeTextWithEscapedCharacters(self, text):

        arr = ['*', "_", "~", "`", "@"]

        for symbol in arr:
            if(symbol in text):
                text = text.replace(symbol, '\\' + symbol)
        
        return text



    def getProfile(self, message):

        self.__userController.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
        user = self.__userController.getUserById(message.from_user.id)

        name = '*Имя*: '
        age = "*Возраст*: "
        description = '*Описание*: '
        sex = '*Пол*: '
        money = '*Бюджет*: '
        marital_status = '*Семейное положение*: '
        stolen_by = "*Кем спрятан*: "

        username = self.__userController.getUserNameById(message.from_user.id)
        name = name + self.takeTextWithEscapedCharacters(username)

        if(user.getAge() == None):
            age = age + "неизвестно"
        else:
            age = age + str(user.getAge())
            
        if(user.getDescription() == None):
            description = description + "отсутствует"
        else: 
            description = description + self.takeTextWithEscapedCharacters(user.getDescription())
            
        if(user.getSex() == None):
            sex = sex + "не указано"
        else: 
            sex = sex + user.getSex().capitalize()
            
        if(user.getMoney() == None):
            money = money + "0 Ⓕ"
        else: 
            money = money + str(user.getMoney()) + " Ⓕ"
            
        if(user.getMaritalStatus() == None):
            marital_status = marital_status + "не указано"
        else: 
            marital_status = marital_status + user.getMaritalStatus()
        
        stolenById = self.__userController.getUserStolenByById(message.from_user.id)
        if(stolenById == None):
            stolen_by = stolen_by + "никем"
        else:
            stolen_by = stolen_by + self.takeTextWithEscapedCharacters(self.__userController.getUserNameById(stolenById))

        return name + '\n' +\
                age + '\n' +\
                description + '\n' +\
                sex + '\n' +\
                money + '\n' +\
                stolen_by
                


    
    def sendProfile(self, message):
        if(message.reply_to_message):
            self.replySmart(message, self.getProfile(message.reply_to_message), self.__keyboardController.startKeyboard())
        else:
            self.replySmart(message, self.getProfile(message), self.__keyboardController.startKeyboard())



    def sendHelp(self, message):

        self.sendSmart(message, "*Команды*:\n\n" + \
            "/register - заполнить профиль\n" +\
            "/myprofile - показать профиль\n" +\
            "/cupboardinfo - вывести информацию\n" +\
            "/buycupboard - купить шкаф (можно иметь только один)\n" +\
            "/sellcupboard - продать шкаф\n" +\
            "`спрятать` - спрятать человека в шкафу\n" +\
            "`выгнать` - выгнать человека из шкафа\n" +\
            "`сбежать` - устроить побег из шкафа\n" +\
            "`освободить шкаф` - полностью освободить шкаф\n\n" +\
            "`перевести КОЛИЧЕСТВО_МОНЕТ` - перевести какое-то количество монет пользователю\n", \
        self.__keyboardController.startKeyboard())

        self.__userController.createUserIfNotExist(message.from_user.id, message.from_user.id)
    


    def sendStart(self, message):

        greetings = ''
        if(self.__userController.checkIfUserExistInDBById(message.from_user.id)):
            greetings = "Сейчас ваш профиль выглядит так: \n\n" + self.getProfile(message) + "\n\n" +\
                "/register - заполнить профиль заново"
        else:
            greetings = "Я заметил, что вы *впервые* пользуетесь моими услугами. Предлагаю *заполнить* профиль, это займет максимум минуту.\n\n" +\
                "/register - заполнить профиль"
        self.sendSmart(message, "Здравствуйте, *" + message.from_user.first_name + "*.\n\n" + greetings +\
            "\n/myprofile - показать ваш *профиль*\n/help - помощь по боту", self.__keyboardController.startKeyboard())
    


    def sendRegister(self, message):

        self.__userController.createUserIfNotExist(message.from_user.id, message.from_user.first_name)

        if(self.checkChatIsPrivate(message)):    

            currentAge = self.__userController.getUserAgeById(message.from_user.id)
            arrAges = []
            if(currentAge != None):
                arrAges = [currentAge]
            else:
                arrAges = ["Пропустить"]

            msg = self.__bot.send_message(message.chat.id, "Сколько вам лет?", reply_markup=self.__keyboardController.createReplyKeyboard(arrAges))
            self.__bot.register_next_step_handler(msg, self.saveAgeAndCreateName)   



    def saveAgeAndCreateName(self, message):
        
        if(message.content_type != "text"):
            msg = self.__bot.send_message(message.chat.id, 'Сообщение должно быть текстовым.', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveAgeAndCreateName)
        elif((message.text.isdigit() == False or (message.text.isdigit() == True and int(message.text) < 1)) and message.text != "Пропустить"):
            msg = self.__bot.send_message(message.chat.id, 'Введите *число* больше 1, пожалуйста.', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveAgeAndCreateName)
        else:
            #ask for name
            arrNames = [message.from_user.first_name]
            currentName = self.__userController.getUserNameById(message.from_user.id)

            if(currentName != message.from_user.first_name and currentName != None):
                arrNames = [message.from_user.first_name, currentName]

            msg = self.__bot.send_message(message.chat.id, "Как вас зовут?", reply_markup=self.__keyboardController.createReplyKeyboard(arrNames))
                
            #save age
            if(message.text != "Пропустить"):
                self.__userController.updateUserAgeById(message.from_user.id, int(message.text))
            else:
                self.__userController.updateUserAgeById(message.from_user.id, None)
            self.__bot.register_next_step_handler(msg, self.saveNameAndCreateDescription)



    def saveNameAndCreateDescription(self, message):

        if(message.content_type != "text"):
            msg = self.__bot.send_message(message.chat.id, 'Сообщение должно быть текстовым.', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveNameAndCreateDescription)
        elif(len(message.text) > 200):
            msg = self.__bot.send_message(message.chat.id, "*Максимальное число символов - 200*. Сократите текст и отправьте *еще раз*.", parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveNameAndCreateDescription)
        else:

            arrDescription = ["Пропустить"]

            if(self.__userController.getUserDescriptionById(message.from_user.id) != None):
                arrDescription = ["Оставить текущий текст", "Пропустить"]

            msg = self.__bot.send_message(message.chat.id, "Напишите что-нибудь о себе.", reply_markup=self.__keyboardController.createReplyKeyboard(arrDescription))
            self.__userController.updateUserNameById(message.from_user.id, message.text)
            self.__bot.register_next_step_handler(msg, self.saveDescriptionAndCreateSex)
    


    def saveDescriptionAndCreateSex(self, message):

        if(message.content_type != "text"):
            msg = self.__bot.send_message(message.chat.id, 'Сообщение должно быть текстовым.', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveDescriptionAndCreateSex)
        elif(len(message.text) > 200):
            msg = self.__bot.send_message(message.chat.id, "*Максимальное число символов - 200*. Сократите текст и отправьте *еще раз*.", parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveDescriptionAndCreateSex)
        else:

            arrSex = ["Мужской", "Женский"]
            msg = self.__bot.send_message(message.chat.id, "Выберите пол.", reply_markup=self.__keyboardController.createReplyKeyboard(arrSex))

            if(message.text == "Пропустить"):
                self.__userController.updateUserDescriptionById(message.from_user.id, None)
            elif(message.text != "Оставить текущий текст"):
                self.__userController.updateUserDescriptionById(message.from_user.id, message.text)

            self.__bot.register_next_step_handler(msg, self.saveSex)
        
    

    def saveSex(self, message):

        if(message.content_type != "text"):
            msg = self.__bot.send_message(message.chat.id, 'Сообщение должно быть текстовым.', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveSex)

        elif(message.text.lower() != "мужской" and message.text.lower() != "женский"):
            msg = self.__bot.send_message(message.chat.id, 'Введите либо "*Мужской*", либо "*Женский*".', parse_mode="Markdown")
            self.__bot.register_next_step_handler(msg, self.saveSex)  

        else:  
            self.__userController.updatetUserSexById(message.from_user.id, message.text)
            status = self.__userController.getUserMaritalStatusById(message.from_user.id)
            
            if(status == None):
                if(message.text.lower() == "мужской"):
                    self.__userController.updateUserMaritalStatusById(message.from_user.id, "Один")
                elif(message.text.lower() == "женский"):
                    self.__userController.updateUserMaritalStatusById(message.from_user.id, "Одна")
            
            self.sendSmart(message, "Данные сохранены. Так выглядит ваш профиль: \n\n" + self.getProfile(message) + "\n\n/register - заполнить профиль заново", \
                self.__keyboardController.startKeyboard())



    def playCasino(self, message):

        text = message.text.split(" ")

        if(text[0].lower() != "казино" and text[0].lower() != "казик"):
            return
        
        if(len(text) != 2 or text[1].isdigit() == False):
            self.__bot.reply_to(message, "Введите `казино СУММА`, где СУММА - целое число.", parse_mode="Markdown")
            return
        
        money = int(text[1]) 

        if(money < 20):
            self.__bot.reply_to(message, "Минимальная сумма - 20 Ⓕ.")
            return

        price = 0
        currentAccount = self.__transactionController.getAccountById(message.from_user.id)

        if(money > currentAccount):
            self.__bot.reply_to(message, "У вас недостаточно средств.")
            return

        chance = secrets.randbelow(999) # random value from 0 to 999

        a = 270 # 27%
        b = a + 100 # 10%
        c = b + 50 # 5%
        d = c + 10 # 1%

        if(chance < a):
            price = money / 2
            self.__transactionController.addMoneyToAccountById(message.from_user.id, price)
            self.__bot.reply_to(message, f"Поздравляю. Вы выиграли {price} Ⓕ.")
        elif(chance > a and chance < b):
            price = money * 1.5
            self.__transactionController.addMoneyToAccountById(message.from_user.id, price)
            self.__bot.reply_to(message, f"Ого! Вы выиграли {price} Ⓕ (шанс этого был 10%)")
        elif(chance > b and chance < c):
            price = money * 3       
            self.__transactionController.addMoneyToAccountById(message.from_user.id, price)
            self.__bot.reply_to(message, f"Ничего себе! Вы выиграли {price} Ⓕ (шанс этого был 5%)") 
        elif(chance > c and chance < d):
            price = money * 10
            self.__transactionController.addMoneyToAccountById(message.from_user.id, price)
            self.__bot.reply_to(message, f"ДЖЕКПОТ! ВЫ ВЫИГРАЛИ {price} Ⓕ!")
        elif(chance == 831):
            price = money * 100
            self.__transactionController.addMoneyToAccountById(message.from_user.id, price)
            self.__bot.reply_to(message, f"КОРОЛЕВСКИЙ ДЖЕКПОТ! ВЫ ВЫИГРАЛИ {price} Ⓕ!")
        else:
            self.__transactionController.takeOffMoneyFromAccountById(message.from_user.id, money)
            self.__bot.reply_to(message, "К сожалению, вы проиграли свои деньги.")
            
    

    def transferMoneyToAnotherAccount(self, message):

        textArr = message.text.lower().split(' ')
        if(len(textArr) != 2 or textArr[0] != "перевести"):
            return
        
        if(message.reply_to_message == None):
            self.__bot.reply_to(message, "Пожалуйста, введите эту команду ответом на сообщение того, кому хотите перевести деньги.")
            return
        
        self.__userController.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
        self.__userController.createUserIfNotExist(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
        
        if(message.from_user.id == message.reply_to_message.from_user.id):
            self.__bot.reply_to(message, "Нельзя перевести деньги себе же.")
            return
        
        if(textArr[1].isdigit() == False):
            self.__bot.reply_to(message, "Пожалуйста, введите корректное значение суммы денег.")
            return
        
        money = int(textArr[1])

        if(money < 10):
            self.__bot.reply_to(message, "Минимальное число для перевода - 10 Ⓕ.")
            return
    
        if(message.reply_to_message.from_user.is_bot == True):
            self.__bot.reply_to(message, self.__exeptionHandler.YouCantUseBot())
            return
        
        codeMessage = self.__transactionController.addMoneyFromAccountToAnotherAccount(message.from_user.id, \
            message.reply_to_message.from_user.id, int(textArr[1]))
        from_user = self.getUserLink(message.from_user.id, self.__userController.getUserNameById(message.from_user.id))
        to_user = self.getUserLink(message.reply_to_message.from_user.id, self.__userController.getUserNameById(message.reply_to_message.from_user.id))

        if(codeMessage == 0):
            self.__bot.send_message(message.chat.id, f"{from_user} успешно перевел {textArr[1]} Ⓕ пользователю {to_user}.", parse_mode="Markdown")
        elif(codeMessage == -1):
            self.__bot.reply_to(message, self.__exeptionHandler.UserNotFoundInDB(from_user), parse_mode="Markdown")
        elif(codeMessage == -2):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveMoneyForTransfering())
        elif(codeMessage == -3):
            self.__bot.reply_to(message, self.__exeptionHandler.UserNotFoundInDB(to_user), parse_mode="Markdown")



    def addMoneyForActivity(self, userId):

        lastcall = self.__userController.getUserLastCallById(userId)

        if(lastcall == None or time.time() - lastcall > 150):
            self.__userController.updateUserLastcallById(userId, time.time())
        elif(time.time() - lastcall > 40 and time.time() - lastcall < 150):

            if(self.__userController.getUserStolenByById(userId) != None):
                self.__transactionController.addMoneyToAccountById(userId, 15)
            else:
                self.__transactionController.addMoneyToAccountById(userId, 30)
            
            self.__userController.updateUserLastcallById(userId, time.time())
    


    def addMoneyWithoutTransactions(self, message):
        text = message.text.split(' ')
        if(len(text) == 2):
            self.__transactionController.addMoneyToAccountById(message.reply_to_message.from_user.id, int(text[1]))
            self.__bot.reply_to(message, f"{self.getUserLink(message.reply_to_message.from_user.id, self.__userController.getUserNameById(message.reply_to_message.from_user.id))} получил(a) {text[1]} Ⓕ.", parse_mode="Markdown")

    

    def deleteUser(self, message):

        userIdForDeleting = 0
        userNameForDeleting = ''

        if(message.reply_to_message):
            userIdForDeleting = message.reply_to_message.from_user.id
            if(self.__userController.checkIfUserExistInDBById(userIdForDeleting) == True):
                userNameForDeleting = self.__userController.getUserNameById(userIdForDeleting)
            else:
                userNameForDeleting = message.reply_to_message.from_user.first_name
        else:
            userIdForDeleting = message.from_user.id
            userNameForDeleting = self.__userController.getUserNameById(userIdForDeleting)
        
        userForDeleting = self.getUserLink(userIdForDeleting, userNameForDeleting)

        if(self.__userController.deleteUserById(userIdForDeleting) == True):
            self.__bot.send_message(\
                message.chat.id,\
                f"Данные пользователя {userForDeleting} успешно удалены.",\
                parse_mode="Markdown")
        else:
            self.__bot.reply_to(message, self.__exeptionHandler.UserNotFoundInDB(userForDeleting), parse_mode="Markdown")



    def doSomething(self, message):

        self.__userController.createUserIfNotExist(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
        arrText = message.text.split(' ')
        verb = arrText[0].lower()
        anotherText = ''

        firstText = ''

        if(verb == "обнять"):
            firstText = "☺️"
        elif(verb == "поцеловать"):
            firstText = "😘"
        elif(verb == "пнуть"):
            firstText = "👟"
        elif(verb == "ударить"):
            firstText = "👊"
        elif(verb == "закрыть"):
            firstText = "🔑"
        elif(verb == "плюнуть"):
            firstText = "🤤"
        else:
            firstText = "🫢"

        for i in arrText:
            if(i != arrText[0]):
                anotherText = anotherText + " " + i

        sex = self.__userController.getUserSexById(message.from_user.id)

        if(sex == None):
            verb = verb[:-2] + "л(а)"
        elif(sex.lower() == "женский"):
            verb = verb[:-2] + "ла"
        else:
            verb = verb[:-2] + "л"
        
        personWhoDo = self.getUserLink(message.from_user.id, self.__userController.getUserNameById(message.from_user.id))
        personToWhom = self.getUserLink(message.reply_to_message.from_user.id, self.__userController.getUserNameById(message.reply_to_message.from_user.id))

        self.__bot.send_message(message.chat.id, f"{firstText} {personWhoDo} {verb} {firstText} {personToWhom}{anotherText}.", parse_mode="Markdown")



    def buyCupboard(self, message):

        text = "Купите шкаф, чтобы прятать туда близких (или не очень) людей:\n\n" +\
            "*Детский шкаф*:\n- 500 Ⓕ\n- вмещает одного человека\n\n" +\
            "*Обычный шкаф*:\n- 1000 Ⓕ\n- вмещает двух человек\n\n" +\
            "*Большой шкаф*:\n- 2000 Ⓕ\n- вмещает четырех человек\n\n" +\
            "Можно иметь только один шкаф.\n/sellcupboard - продать шкаф\n`спрятать` - спрятать человека"
        self.__bot.send_message(message.chat.id, text, reply_markup=self.__keyboardController.cupboardKeyboad(), parse_mode="Markdown") 
    


    def sellCupboard(self, message):
        userId = message.from_user.id
        cupboardInfo = self.__cupboardController.getInfoAboutCupboardById(userId)

        if(cupboardInfo == None):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveCupboard())
            return
        
        price = 0

        if(cupboardInfo == "Детский"):
            price = 500
        elif(cupboardInfo == "Обычный"):
            price = 1000
        elif(cupboardInfo == "Большой"):
            price = 2000
        else:
            self.__bot.reply_to(message, self.__exeptionHandler.YouCantSellCupboard())
            return
        
        text = f"Вы успешно продали *{cupboardInfo} шкаф* и получили {price} Ⓕ.\n" +\
            "Чтобы купить шкаф, введите:\n/buycupboard"
        
        self.__transactionController.addMoneyToAccountById(userId, price)
        self.__userController.updateUserCupboardById(userId, None)
        self.__bot.reply_to(message, text, parse_mode="Markdown")



    def hideInCupboard(self, message):
        
        if(message.reply_to_message == None):
            self.__bot.reply_to(message, self.__exeptionHandler.AnswerOnUserMessage())
            return
        
        if(message.reply_to_message.from_user.is_bot == True and message.from_user.id != Resources.main_id):
            self.__bot.reply_to(message, "Нельзя спрятать бота.")
            return

        hiderId = message.from_user.id
        size = 0
        typeCup = self.__cupboardController.getCupboardTypeById(hiderId)
        usersArr = self.__cupboardController.getUsersFromCupboardById(hiderId)

        if(typeCup == "Детский"):
            size = 1
        elif(typeCup == "Обычный"):
            size = 2
        elif(typeCup == "Большой"):
            size = 4
        
        if(usersArr != None and len(usersArr) == size):
            self.__bot.reply_to(message, "Ваш шкаф полон.")
            return

        if(self.__userController.getUserMoneyById(hiderId) < 150):
            self.__bot.reply_to(message, "У вас не хватает средств. Для того, чтобы спрятать человека, необходимо оборудование на сумму 150 Ⓕ.")
            return

        hidenId = message.reply_to_message.from_user.id
        status = self.__cupboardController.hideUserInCupboard(hiderId, hidenId)

        if(status == -1):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveCupboard())

        elif(status == -2):
            self.__bot.reply_to(message, self.__exeptionHandler.YouCanHideYourself())

        elif(status == -3):
            hidenById = self.__userController.getUserStolenByById(hidenId)
            hidenByName = self.__userController.getUserNameById(hidenById)
            hidenBy = self.getUserLink(hidenById, hidenByName)
            self.__bot.reply_to(message, self.__exeptionHandler.UserIsAlreadyHiden(hidenBy), parse_mode="Markdown")

        elif(status == 0):

            self.__transactionController.takeOffMoneyFromAccountById(hiderId, 150)

            if(self.getTrueWithLuck(90) == False):
                self.__bot.reply_to(message, self.__exeptionHandler.HidingFailure())
                self.__cupboardController.expelUserFromKupboardById(hiderId, hidenId)
                return

            hider = self.getUserLink(hiderId, self.__userController.getUserNameById(hiderId))
            hiden = self.getUserLink(hidenId, self.__userController.getUserNameById(hidenId))
            sex = self.__userController.getUserSexById(hiderId)

            word = ""
            if(sex == None):
                word = "спрятал(а)"
            elif(sex.lower() == "мужской"):
                word = "спрятал"
            elif(sex.lower() == "женский"):
                word = "спрятала"

            self.__bot.send_message(message.chat.id,\
                f"{hider} {word} в шкафу {hiden}. Теперь {hiden} будет получать в два раза меньше денег за активность до тех пор, пока не окажется на свободе.\n/runaway - попытаться сбежать",\
                parse_mode="Markdown")



    def sendCupboardInfo(self, message):

        id = message.from_user.id
        if(self.__cupboardController.checkIfUserHaveCupboard(id) == False):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveCupboard())
            return
        
        typeCup = self.__cupboardController.getCupboardTypeById(id)
        size = 0

        if(typeCup == "Детский"):
            size = 1
        elif(typeCup == "Обычный"):
            size = 2
        elif(typeCup == "Большой"):
            size = 4
        
        usersArr = self.__cupboardController.getUsersFromCupboardById(id)
        sizeUsers = 0

        if(usersArr == None):
            sizeUsers = 0
        else:
            sizeUsers = len(usersArr)

        text = "Тип: *" + typeCup + "*\n\n" 
    
        i = 0
        while(i < size):

            if(i < sizeUsers):

                userId = int(usersArr[i])
                if(message.chat.id > 0):
                    text = text + f"{i + 1}. {self.getUserLink(userId, self.__userController.getUserNameById(userId))}\n"
                else:
                    text = text + f"{i + 1}. *{self.__userController.getUserNameById(userId)}*\n"

            else:
                text = text + f"{i + 1}. \[пусто]\n"
            i = i + 1 
        
        self.__bot.reply_to(message, text, parse_mode="Markdown")
    


    def freeCupboard(self, message):

        users = self.__cupboardController.getUsersFromCupboardById(message.from_user.id)
        status = self.__cupboardController.freeCupboardById(message.from_user.id)
        hider = self.getUserLink(message.from_user.id, self.__userController.getUserNameById(message.from_user.id))

        if(status == 0):
            self.__bot.reply_to(message, "Ваш шкаф успешно освобожден.")

            sex = self.__userController.getUserSexById(message.from_user.id)    
            word = ''        

            if(sex == None):
                word = "освободил(а)"
            elif(sex.lower() == "мужской"):
                word = "освободил"
            elif(sex.lower() == "женский"):
                word = "освободила"

            for user in users:
                try:
                    self.__bot.send_message(int(user), f"{hider} {word} шкаф. Теперь вы свободны.", parse_mode="Markdown")
                except:
                    print("Error: Bot can't initiate conversation with a user.")


        elif(status == -1):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveCupboard())
        elif(status == -2):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHidenAnyone())
        


    def expelFromCupboard(self, message):

        if(message.reply_to_message == None):
            self.__bot.reply_to(message, self.__exeptionHandler.AnswerOnUserMessage())
            return
        
        ownerId = message.from_user.id
        hidenId = message.reply_to_message.from_user.id

        status = self.__cupboardController.expelUserFromKupboardById(ownerId, hidenId)

        if(status == 0):

            owner = self.getUserLink(ownerId, self.__userController.getUserNameById(ownerId))
            hiden = self.getUserLink(hidenId, self.__userController.getUserNameById(hidenId))
            word = ''
            sex = self.__userController.getUserSexById(ownerId)
            
            if(sex == None):
                word = "выгнал(а)"
            elif(sex.lower() == "мужской"):
                word = "выгнал"
            elif(sex.lower() == "женский"):
                word = "выгнала"

            self.__bot.send_message(message.chat.id, f"{owner} {word} пользователя {hiden} из шкафа.", parse_mode="Markdown")
        
        elif(status == -1):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveCupboard())
        
        elif(status == -2):
            self.__bot.reply_to(message, "Вы не можете выгнать себя же.")
        
        elif(status == -3):
            self.__bot.reply_to(message, self.__exeptionHandler.YourCupboardIsEmpty())
        
        elif(status == -4):
            self.__bot.reply_to(message, self.__exeptionHandler.YouDontHidenThisUser())



    def runawayFromCupboard(self, message):

        hidenId = message.from_user.id
        hiderId = self.__userController.getUserStolenByById(hidenId)

        if(hiderId == None):
            self.__bot.reply_to(message, self.__exeptionHandler.NooneHideYou())
            return 
        
        money = self.__transactionController.getAccountById(hidenId)

        if(money < 100):
            self.__bot.reply_to(message, "Не хватает средств. Для побега необходимо 100 Ⓕ.")
            return
        
        self.__transactionController.takeOffMoneyFromAccountById(hidenId, 100)

        if(self.getTrueWithLuck(60) == False):
            self.__bot.reply_to(message, self.__exeptionHandler.EscapingFailure())
            return

        self.__cupboardController.expelUserFromKupboardById(hiderId, hidenId)
        self.__bot.reply_to(message, "Побег удался.")


        sex = self.__userController.getUserSexById(hidenId)            
        if(sex == None):
            word = "сбежал(а)"
        elif(sex.lower() == "мужской"):
            word = "сбежал"
        elif(sex.lower() == "женский"):
            word = "сбежала"

        try:
            self.__bot.send_message(hiderId, f"{self.getUserLink(hidenId, self.__userController.getUserNameById(hidenId))} {word} из вашего шкафа.", parse_mode="Markdown")
        except:
            print("Error: Bot can't initiate conversation with a user.")


    def buyCupboardWithChoosing(self, typeCupboard, price, message):

        if(self.__cupboardController.checkIfUserHaveCupboard(message.from_user.id) == False):
            
            status = self.__transactionController.takeOffMoneyFromAccountById(message.from_user.id, price)

            if(status == 0):
                self.__userController.updateUserCupboardById(message.from_user.id, typeCupboard)
                self.__bot.reply_to(message, f"Вы успешно приобрели *{typeCupboard} шкаф* за {price} Ⓕ. Чтобы спрятать кого-нибудь в нем, " +\
                    "введите `спрятать` ответом на сообщение человека, которого хотите спрятать.", parse_mode="Markdown")

            elif(status == -2):
                self.__bot.reply_to(message, self.__exeptionHandler.YouDontHaveMoney())

        else:
            self.__bot.reply_to(message, self.__exeptionHandler.YouAlreadyHaveCupboard())


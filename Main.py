import telebot
from telebot import types

from models.User import User
from resources.Resources import Resources
from services.UserService import UserService

bot = telebot.TeleBot(Resources.token)
UserService = UserService()


def checkChatIsPrivate(message):
    if(message.chat.id < 0):
        bot.reply_to(message, "Введите эту команду в чате со мной, пожалуйста.")
        return False
    
    return True


def getProfile(message):

    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
    user = UserService.getUserById(message.from_user.id)

    name = '*Имя*: '
    description = '*Описание*: '
    sex = '*Пол*: '
    money = '*Бюджет*: '
    marital_status = '*Семейное положение*: '
    job = '*Профессия*: '

    if(user.getName() == None):
        name = name + message.from_user.first_name 
    else:
        name = name + user.getName()
        
    if(user.getDescription() == None):
        description = description + "[отсутствует]"
    else: 
        description = description + user.getDescription()
        
    if(user.getSex() == None):
        sex = sex + "[не указано]"
    else: 
        sex = sex + user.getSex()
        
    if(user.getMoney() == None):
        money = money + "0 Ⓕ"
    else: 
        money = money + str(user.getMoney()) + " Ⓕ"
        
    if(user.getMaritalStatus() == None):
        marital_status = marital_status + "[не указано]"
    else: 
        marital_status = marital_status + user.getMaritalStatus()
        
    if(user.getJob() == None):
        job = job + "безработный"
    else: 
        job = job + user.getJob()

    return name + '\n' +\
            description + '\n' +\
            sex + '\n' +\
            money + '\n' +\
            marital_status + '\n' +\
            job


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id, "*Команды*:\n\n" + \
        "/register - заполнить профиль\n" +\
        "/myprofile - показать профиль\n" +\
        "", parse_mode="Markdown")
    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)


@bot.message_handler(commands=["start"])
def send_start(message):

    if(message.chat.id > 0):
        greetings = ''

        if(UserService.checkIfUserExistInDB(message.from_user.id)):
            greetings = "Сейчас ваш профиль выглядит так: \n\n" + getProfile(message) + "\n\n" +\
                "/register - заполнить профиль заново"
        else:
            greetings = "Я заметил, что вы *впервые* пользуетесь моими услугами. Предлагаю *заполнить* профиль, это займет максимум минуту.\n\n" +\
                "/register - заполнить профиль"

        bot.send_message(message.chat.id, "Здравствуйте, *" + message.from_user.first_name + "*.\n\n" + greetings + "\n/myprofile - показать ваш *профиль*", parse_mode="Markdown")


@bot.message_handler(commands=["register"])
def send_register(message):
    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
    if(checkChatIsPrivate(message)):

        msg = bot.send_message(message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(msg, saveNameAndCreateDescription)
        

def saveNameAndCreateDescription(message):
    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
    if(checkChatIsPrivate(message)):

        UserService.updateNameById(message.from_user.id, message.text)
        msg = bot.send_message(message.chat.id, "Напишите что-нибудь о себе.")
        bot.register_next_step_handler(msg, saveDescriptionAndCreateSex)


def saveDescriptionAndCreateSex(message):
    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
    if(checkChatIsPrivate(message)):

        UserService.updateDescriptionById(message.from_user.id, message.from_user.first_name, message.text)
        msg = bot.send_message(message.chat.id, "Выберите пол.")
        bot.register_next_step_handler(msg, saveSex)


def saveSex(message):
    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)
    if(checkChatIsPrivate(message)):

        if(message.text.lower() != "мужской" and message.text.lower() != "женский"):

            msg = bot.send_message(message.chat.id, 'Введите либо "*Мужской*", либо "*Женский*".', parse_mode="Markdown")
            bot.register_next_step_handler(msg, saveSex)  
        else:  

            UserService.updateSexById(message.from_user.id, message.from_user.first_name, message.text)
            bot.send_message(message.chat.id, "Данные сохранены. Так выглядит ваш профиль: \n\n" + getProfile(message) + "\n\n/register - заполнить профиль заново", parse_mode="Markdown")

            user = UserService.getUserById(message.from_user.id)

            if(user.getMaritalStatus() == None):
                if(message.text.lower() == "мужской"):
                    UserService.updateMaritalStatusById(message.from_user.id, message.from_user.first_name, "Один")
                elif(message.text.lower() == "женский"):
                    UserService.updateMaritalStatusById(message.from_user.id, message.from_user.first_name, "Одна")


@bot.message_handler(content_types=['text'])
def send_text(message):

    UserService.createUserIfNotExist(message.from_user.id, message.from_user.first_name)

    if(message.text == "/myprofile"):
        bot.send_message(message.chat.id, getProfile(message), parse_mode="Markdown")
    
    elif("+столбец" in message.text and message.from_user.id == Resources.main_id):
        wordsInMessage = message.text.split(' ')
        if(len(wordsInMessage) == 3):
            UserService.addColumn(wordsInMessage[1], wordsInMessage[2])
            bot.send_message(message.chat.id, f"Столбец {wordsInMessage[1]} с типом данных {wordsInMessage[2]} успешно создан.")
        else:
            bot.send_message(message.chat.id, f"Столбец не создан. Проверьте написание команды:\n" + \
                "`+столбец НАЗВАНИЕ_СТОЛБЦА ТИП_ДАННЫХ`", parse_mode="Markdown")



    
bot.infinity_polling(timeout=10, long_polling_timeout = 5)

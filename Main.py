import telebot

from resources.Resources import Resources

from controllers.ChatController import ChatController
from controllers.UserController import UserController

bot = telebot.TeleBot(Resources.:AAEs_uzb5_9Fso_1x7qwIkpBljHlNdrHYTw)

chatController = ChatController(https://t.me/Fillla_Bot)
userController = UserController(5625164134)


@bot.message_handler(commands=["help"])
def send_help(message):
    chatController.sendHelp(message)



@bot.message_handler(commands=["start"])
def send_start(message):
    chatController.sendStart(message)



def commandNotExist(message):
    bot.reply_to(message, "Данная команда сейчас не доступна. Извините за неудобства.")



@bot.message_handler(content_types=['text'])
def send_text(message):

    userController.createUserIfNotExist(message.from_user.id, message.from_user.first_name)

    if(message.reply_to_message):
        userController.createUserIfNotExist(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)

    chatController.addMoneyForActivity(message.from_user.id)

    if(message.reply_to_message == None and (message.text == "/myprofile" or message.text == "/myprofile@fillatovbot" or message.text.lower() == "профиль" or message.text.lower() == "мой профиль" or message.text.lower() == "кто я")):
        chatController.sendProfile(message)

    elif(message.reply_to_message and (message.text.lower() == "твой профиль" or message.text.lower() == "профиль" or message.text.lower() == "кто ты")):
        chatController.sendProfile(message)
    
    elif(("казино" in message.text.lower() or "казик" in message.text.lower()) and len(message.text) < 30):
        chatController.playCasino(message)

    elif(message.text == "/register" or message.text == "/register@fillatovbot" or message.text.lower() == "заполнить профиль"):
        chatController.sendRegister(message)
    
    elif(len(message.text) < 20 and "перевести" in message.text.lower()):
        chatController.transferMoneyToAnotherAccount(message)
    
    elif(message.text.lower() == "купить шкаф" or message.text == "/buycupboard" or message.text == "/buycupboard@fillatovbot"):
        chatController.buyCupboard(message)
    
    elif(message.text.lower() == "продать шкаф" or message.text == "/sellcupboard" or message.text == "/sellcupboard@fillatovbot"):
        chatController.sellCupboard(message)
    
    elif(message.text.lower() == "шкаф инфо" or message.text == "/cupboardinfo" or message.text == "/cupboardinfo@fillatovbot" or message.text.lower() == "мой шкаф"):
        chatController.sendCupboardInfo(message)
    
    elif(message.text.lower() == "выгнать" or message.text == "освободить" or message.text == "выкинуть" or message.text == "/expel" or message.text == "/expel@fillatovbot"):
        chatController.expelFromCupboard(message)
    
    elif(message.text == "/freecupboard" or message.text == "/freecupboard@fillatovbot" or message.text.lower() == "освободить шкаф"):
        chatController.freeCupboard(message)
    
    elif(message.text == "/hide" or message.text == "/hide@fillatovbot" or message.text.lower() == "спрятать"):
        chatController.hideInCupboard(message)
    
    elif(message.text == "/runaway" or message.text == "/runaway@fillatovbot" or message.text.lower() == "сбежать" or message.text.lower() == "убежать"):
        chatController.runawayFromCupboard(message)
    
    elif(message.text == "@fillatovbot Купить детский шкаф" or message.text.lower() == "купить детский шкаф"):
        chatController.buyCupboardWithChoosing("Детский", 500, message)
        
    elif(message.text == "@fillatovbot Купить обычный шкаф" or message.text.lower() == "купить обычный шкаф"):
        chatController.buyCupboardWithChoosing("Обычный", 1000, message)
        
    elif(message.text == "@fillatovbot Купить большой шкаф" or message.text.lower() == "купить большой шкаф"):
        chatController.buyCupboardWithChoosing("Большой", 2000, message)

    elif(message.reply_to_message and message.text[0] == "+" and message.from_user.id == Resources.main_id):
        chatController.addMoneyWithoutTransactions(message)

    elif(message.text == "/reset" and message.from_user.id == Resources.main_id):
        chatController.deleteUser(message)

    else:

        if(message.reply_to_message and len(message.text) < 200):
            verb = message.text.split(' ')[0].lower()
            verbs = ["закрыть", "убить", "покормить", "напоить", "кинуть", "открыть", "обнять", "поцеловать", "ударить", \
                "пнуть", "плюнуть", "взять", "атаковать", "укусить", "дать", "похвалить", "поздравить", "сломать"]
            if(verb[-2:] == "ть" and (verb in verbs)):
                chatController.doSomething(message)



@bot.message_handler(content_types=['audio', 'document', 'voice', 'video_note', 'photo', 'video'])
def send_files(message):
    chatController.addMoneyForActivity(message.from_user.id)


    
bot.infinity_polling(timeout=10, long_polling_timeout = 5)

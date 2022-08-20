from telebot import types

class KeyboardService:
    
    def createReplyKeyboard(self, textArray):

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for text in textArray:
            markup.add(types.KeyboardButton(text))
        
        return markup
    

        

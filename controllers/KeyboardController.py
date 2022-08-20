from telebot import types

from services.KeyboardService import KeyboardService
from resources.Resources import Resources

class KeyboardController:

    __keyboardService = KeyboardService()


    def createReplyKeyboard(self, textArray):
        return self.__keyboardService.createReplyKeyboard(textArray)


    def startKeyboard(self):

        arr = ["Заполнить профиль", "Мой профиль"]
        return self.__keyboardService.createReplyKeyboard(arr)
    

    def goToBotKeyboard(self):

        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти к боту", url=Resources.url)
        keyboard.add(url_button)

        return keyboard


    def cupboardKeyboad(self):

        keyboard = types.InlineKeyboardMarkup()
        child = types.InlineKeyboardButton(text="Детский шкаф", switch_inline_query_current_chat="Купить детский шкаф")
        usual = types.InlineKeyboardButton(text="Обычный шкаф", switch_inline_query_current_chat="Купить обычный шкаф")
        big = types.InlineKeyboardButton(text="Большой шкаф", switch_inline_query_current_chat="Купить большой шкаф")
        keyboard.add(child).add(usual).add(big)

        return keyboard


class ExeptionHandler:

    def YouCantUseBot(self):
        return "Взаимодействовать с ботом нельзя."
    
    def AnswerOnUserMessage(self):
        return "Пожалуйста, введите эту команду ответом на сообщение того, с кем хотите взаимодействовать."
    
    def UserNotFoundInDB(self, user):
        return f"{user} не имеет профиля. Для того, чтобы создался профиль, пользователь должен ввести любое сообщение в чат."
    
    def YouDontHaveMoneyForTransfering(self):
        return "У вас недостаточно средств для перевода\n/myprofile - показать профиль"
    
    def YouDontHaveMoney(self):
        return "У вас недостаточно средств.\n/myprofile - показать профиль"
    
    def YouDontHaveCupboard(self):
        return "Вы еще не приобрели шкаф. Для того, чтобы купить, введите:\n/buycupboard"
    
    def YouAlreadyHaveCupboard(self):
        return "У вас уже есть шкаф. Чтобы купить новый, необходимо продать имеющийся.\n\n/sellcupboard - продать шкаф"
    
    def HidingFailure(self):
        return "К сожалению, прятки пошли не по плану. Попытка спрятать человека провалилась."
    
    def EscapingFailure(self):
        return "К сожалению, попытка побега провалилась."
    
    def YouCanHideYourself(self):
        return "Вы не можете украсть самого себя."
    
    def UserIsAlreadyHiden(self, hidenBy):
        return f"{hidenBy} уже спрятал этого пользователя в своем шкафу."
    
    def YouDontHidenAnyone(self):
        return "Вы еще никого не спрятали."
    
    def YouDontHidenThisUser(self):
        return "Этого пользователя нет в вашем шкафу."
    
    def YourCupboardIsEmpty(self):
        return "Ваш шкаф пуст."
    
    def NooneHideYou(self):
        return "Вас никто не прятал."
    
    def YouCantSellCupboard(self):
        return "Вы не можете продать шкаф, пока там находятся люди. Освободите шкаф командами:\n/expel - выгнать пользователя\n/freecupboard - выгнать всех"

class BankAccount:
    def __init__(self, card_number, holder):
        self.card_number = card_number
        self.holder = holder
        # Инкапсуляция: __balance скрыт от прямого изменения извне
        self.__balance = 0
        self._history = [] # Защищенный атрибут для истории

    # Геттер для баланса
    @property
    def balance(self):
        return self.__balance

    # Сеттер для баланса (защита от отрицательных значений)
    @balance.setter
    def balance(self, value):
        if value < 0:
            print(f"⚠️ Ошибка: Баланс {self.holder} не может быть отрицательным!")
        else:
            self.__balance = value

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount # Используем сеттер
            self._history.append(f"Пополнение: +{amount}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount # Используем сеттер
            self._history.append(f"Снятие: -{amount}")
            return True
        print(f"❌ Недостаточно средств на счете {self.holder}")
        return False

    def show_history(self):
        print(f"\n--- 📜 История: {self.holder} ---")
        for op in self._history:
            print(op)

# Наследование: Детский аккаунт с лимитом
class KidsAccount(BankAccount):
    def __init__(self, card_number, holder, limit=500):
        super().__init__(card_number, holder)
        self.limit = limit

    def withdraw(self, amount):
        if amount > self.limit:
            print(f"❌ Лимит превышен! (Макс: {self.limit})")
            return False
        return super().withdraw(amount)

# Наследование: Золотой аккаунт (Кэшбэк при пополнении)
class GoldAccount(BankAccount):
    def deposit(self, amount):
        # Привилегия: +1% к любому пополнению
        bonus = amount * 0.01
        total = amount + bonus
        print(f"✨ Gold-бонус начислен: {bonus}")
        return super().deposit(total)

# Метод перевода (внешняя функция для демонстрации взаимодействия)
def transfer(from_acc, to_acc, amount):
    print(f"\n💸 Перевод: {from_acc.holder} -> {to_acc.holder} ({amount} руб.)")
    if from_acc.withdraw(amount):
        if to_acc.deposit(amount):
            print("✅ Перевод выполнен успешно!")
            return True
        else:
            print("⚠️ Ошибка зачисления. Возврат средств...")
            from_acc.deposit(amount)
    return False

# --- Сценарий для портфолио ---
if __name__ == "__main__":
    artem = KidsAccount(101, "Артем", limit=300)
    ivan = GoldAccount(202, "Иван")

    ivan.deposit(1000) # Иван получит 1010 из-за Gold-статуса
    transfer(ivan, artem, 500) # У Ивана спишется, у Артема зачислится
    
    artem.withdraw(400) # Ошибка лимита (лимит 300)
    artem.show_history()
    ivan.show_history()

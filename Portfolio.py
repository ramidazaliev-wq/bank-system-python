class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
        self._history = [f"🏁 Счет создан. Владелец: {owner}. Начальный баланс: {balance}"]

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._history.append(f"📥 Пополнение: +{amount}. Итог: {self._balance}")
            print(f'💰 {self.owner}: +{amount}')
        else:
            print("❌ Ошибка: сумма пополнения должна быть больше 0!")

    def withdraw(self, amount):
        total_cost = amount * 1.01
        if amount > 0 and total_cost <= self._balance:
            self._balance -= total_cost
            self._history.append(f"📤 Снятие: -{amount} (комиссия: {round(amount * 0.01, 2)}). Итог: {self._balance}")
            print(f"✅ {self.owner} снял {amount}. (Комиссия 1%)")
        else:
            print(f"❌ {self.owner}: Недостаточно средств (нужно {total_cost} с учетом комиссии).")

    def transfer(self, target_account, amount):
        total_cost = amount * 1.01

        if target_account == self:
            print(f"⚠️ {self.owner}, нельзя переводить деньги самому себе!")
            return

        if amount > 0 and total_cost <= self._balance:
            self._balance -= total_cost
            self._history.append(
                f"✈️ Перевод: -{amount} для {target_account.owner} (комиссия {round(amount * 0.01, 2)}). Итог: {self._balance}")

            # Зачисляем деньги получателю
            target_account.deposit(amount)
            print(f"✈️ Перевод выполнен: {self.owner} -> {target_account.owner} ({amount} руб.)")
        else:
            print(f"❌ Перевод от {self.owner} отклонен: недостаточно средств.")

    def show_history(self):
        print(f"\n📜 ИСТОРИЯ ОПЕРАЦИЙ КЛИЕНТА {self.owner.upper()}:")
        for record in self._history:
            print(f"  -> {record}")
        print("-" * 40)

    def show_info(self):
        print(f"👤 {self.owner} | 💰 Текущий баланс: {self._balance}")


class KidsAccount(BankAccount):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)
        self.limit = 500

    def withdraw(self, amount):
        if amount > self.limit:
            print(f"❌ Ошибка! Маленьким нельзя снимать больше {self.limit} руб. (запрос: {amount})")
        else:

            super().withdraw(amount)


class GoldAccount(BankAccount):
    def __init__(self, owner, balance=0):
        super().__init__(owner, balance)
        self.fee = 200
        if self._balance >= self.fee:
            self._balance -= self.fee
            self._history.append(f"✨ Списано за открытие Gold-статуса: -{self.fee}. Итог: {self._balance}")
            print(f"\n✨ Открыт Gold-счет для {self.owner}! Списано: {self.fee}")
        else:
            print(f"⚠️ Внимание: баланс {self.owner} меньше стоимости обслуживания!")

    def withdraw(self, amount):
        """У Gold-клиентов снятие БЕЗ комиссии"""
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self._history.append(f"👑 Gold-снятие: -{amount} (Без комиссии). Итог: {self._balance}")
            print(f"👑 {self.owner}: снято {amount} руб. без комиссии.")
        else:
            print(f"❌ Gold-отказ для {self.owner}: недостаточно средств.")

    def apply_interest(self):
        """Начисление 10% годовых на остаток (бонус Gold-статуса)"""
        bonus = round(self._balance * 0.10, 2)
        if bonus > 0:
            self._balance += bonus
            self._history.append(f"📈 Начисление процентов (10%): +{bonus}. Итог: {self._balance}")
            print(f"📈 {self.owner}: начислено {bonus} руб. годовых.")





artem = KidsAccount("Артем", 1000)
petr = GoldAccount("Петр", 5000)
ivan = BankAccount("Иван", 2000)

artem.withdraw(600)
ivan.transfer(artem, 300)


petr.withdraw(1000)
petr.apply_interest()


print("\n--- ИТОГИ ---")
artem.show_info()
petr.show_info()
ivan.show_info()


petr.show_history()
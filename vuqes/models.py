from django.db import models, transaction
from django.conf import settings


class BankAccount(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Баланс')
    image = models.ImageField(null=True, upload_to='vuqes/%Y/%m/%d')
    city = models.CharField(max_length=50, verbose_name='Город проживания')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Transaction(models.Model):
    recipient = models.ForeignKey('BankAccount', on_delete=models.CASCADE, verbose_name='Получатель')
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Сумма перевода')
    date_transaction = models.DateTimeField(auto_now_add=True, null=True)
    sender = models.CharField(max_length=255)
    is_success = models.BooleanField(default=False)

    @classmethod
    def do_transaction(cls, recipient, value, sender):
        sender_acc = BankAccount.objects.get(pk=sender)
        with transaction.atomic():
            if sender_acc.balance < value:
                raise ValueError('Недостаточно средств')
            else:
                recipient.balance += value
                sender_acc.balance -= value
                recipient.save()
                sender_acc.save()
        return recipient, value


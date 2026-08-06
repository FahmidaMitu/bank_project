import random
from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_holder_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(random.randint(1000000000, 9999999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.account_holder_name}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    )

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-timestamp'] # Newest first

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount}"
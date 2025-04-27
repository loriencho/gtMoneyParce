from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = 'user', 'name'

    def __str__(self):
        return f"{self.name}"

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Transaction(models.Model):
    # Income or Expense
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # User input
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Category input
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # In/Out input
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    # Amount input
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    # Date input
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} of {self.amount} on {self.date} by {self.user}"

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_list = models.ManyToManyField(Transaction, blank=True)
    category_list = models.ManyToManyField(Category, blank=True)
    income = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    expense = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    budget = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f"{self.user}'s account"
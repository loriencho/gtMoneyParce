from dateutil.relativedelta import relativedelta
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
    # ID
    id = models.AutoField(primary_key=True)

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

    def calculate_income(self):
        self.income = 0
        for transaction in self.transaction_list.filter(type='income'):
            self.income += transaction.amount
        self.save()
        return self.income

    def calculate_expense(self):
        self.expense = 0
        for transaction in self.transaction_list.filter(type='expense'):
            self.expense += transaction.amount
        self.save()
        return self.expense

    def calculate_total(self):
        return self.income - self.expense

    def over_budget(self, date):
        return self.monthly_expenses(date) > self.budget

    def monthly_income(self, date):
        income = 0
        for transaction in self.transaction_list.filter(type='income'):
            if transaction.date >= date and transaction.date <= (date + relativedelta(months=+1)):
                income += transaction.amount
        return income

    def monthly_expenses(self, date):
        expenses = 0
        for transaction in self.transaction_list.filter(type='expense'):
            if transaction.date >= date and transaction.date <= (date + relativedelta(months=+1)):
                expenses += transaction.amount
        return expenses
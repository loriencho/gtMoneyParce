from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from financials.forms import TransactionForm, EditTransactionForm, BudgetForm, GraphTypeForm
from financials.models import Transaction, Category, Account
from decimal import Decimal
import json
import datetime
from dateutil.relativedelta import relativedelta

current_date = datetime.date.today().replace(day=1)
graph_type = 'Total'

@login_required
def dashboard(request):
    context = {}
    context['title'] = 'Money Parce'
    global current_date
    global graph_type


    account, _ = Account.objects.get_or_create(user=request.user)
    transactions = account.transaction_list.all()
    context['transactions'] = transactions
    context['account'] = account

    if request.method == 'GET':
        if request.GET.get('btn') == 'Prev':
            current_date = (current_date + relativedelta(months=-1)).replace(day=1)
        elif request.GET.get('btn') == 'Next':
            current_date = (current_date + relativedelta(months=+1)).replace(day=1)
        elif request.GET.get('btn') == 'Totals':
            graph_type = 'Totals'
        elif request.GET.get('btn') == 'Categories':
            graph_type = 'Categories'

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            account.budget = budget
            account.save()

    context['graph_type'] = graph_type
    context['current_date'] = current_date.strftime('%B %Y')

    total_expenses = account.monthly_expenses(current_date)
    total_income = account.monthly_income(current_date)

    context['total_expenses'] = total_expenses
    context['total_income'] = total_income

    if total_expenses > total_income:
        advice = "You are spending more than you are earning. Consider budgeting better or reducing expenses."
    elif total_expenses > Decimal('0.8') * total_income:
        advice = "You're spending a large part of your income. Try to save more!"
    elif total_expenses < Decimal('0.5') * total_income:
        advice = "Good job! You’re saving a good amount of your income!"
    else:
        advice = "Your spending is balanced with your income."

    context['advice'] = advice

    category_totals = {}
    for transaction in transactions.filter(type='expense'):
        if transaction.date >= current_date and transaction.date <= (current_date + relativedelta(months=+1)):
            cat_name = transaction.category.name
            if cat_name not in category_totals:
                category_totals[cat_name] = 0
            category_totals[cat_name] += transaction.amount

    context['category_totals'] = category_totals
    context['category_totals_keys'] = json.dumps(list(category_totals.keys()))
    context['category_totals_values'] = json.dumps([float(val) for val in category_totals.values()])

    context['budgetform'] = BudgetForm()
    context['overbudget'] = account.over_budget(current_date)

    return render(request, 'financials/dashboard.html', {'context': context})


@login_required
def transactions_list(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    categories = account.category_list.all()
    context = {}
    filter_list = []
    inout_list = []

    for category in categories:
        if request.GET.get(str(category.id)):
            filter_list.append(category.name)
    if request.GET.get('Income'):
        inout_list.append('income')
    if request.GET.get('Expense'):
        inout_list.append('expense')
    if filter_list:
        transactions = account.transaction_list.filter(category__name__in=filter_list, type__in=inout_list)
    elif inout_list:
        transactions = account.transaction_list.filter(type__in=inout_list)
    else:
        transactions = account.transaction_list.all()

    context['transactions'] =  transactions
    context['categories'] = categories

    return render(request, 'financials/transactions-list.html', context)

@login_required
def add_transaction(request):
    context = {}
    context['form'] = TransactionForm(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            account, _ = Account.objects.get_or_create(user=request.user)
            if form.cleaned_data['new_category']:
                category, _ = account.category_list.get_or_create(name=form.cleaned_data['new_category'])
            else:
                category = form.cleaned_data['category']
                if not category:
                    category, _ = account.category_list.get_or_create(name="Uncategorized")[0]
            transaction = Transaction(
                user=request.user,
                amount=abs(form.cleaned_data['amount']),
                type=form.cleaned_data['type'],
                category=category,
                date=form.cleaned_data['date'],
            )
            transaction.save()
            account.transaction_list.add(transaction)
            return redirect('financials.transactions-list')
    return render(request, 'financials/add-transaction.html', context)

@login_required
def edit_transaction(request, transaction_id):
    context = {}
    transaction = get_object_or_404(Transaction, id=transaction_id)
    context['form'] = EditTransactionForm(user=request.user, old=transaction)
    if request.user != transaction.user:
        return redirect('financials.transactions-list')
    if request.method == 'POST':
        form = EditTransactionForm(user=request.user, old=transaction, data=request.POST)
        if form.is_valid():
            account, _ = Account.objects.get_or_create(user=request.user)
            if form.cleaned_data['new_category']:
                category = Category.objects.get_or_create(name=form.cleaned_data['new_category'])
            else:
                category = form.cleaned_data['category']
                if not category:
                    category, _ = account.category_list.get_or_create(name="Uncategorized")[0]

            transaction.amount = abs(form.cleaned_data['amount'])
            transaction.type = form.cleaned_data['type']
            transaction.category = category
            transaction.date = form.cleaned_data['date']
            transaction.save()
            return redirect('financials.transactions-list')
    return render(request, 'financials/add-transaction.html', context)

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect('financials.transactions-list')

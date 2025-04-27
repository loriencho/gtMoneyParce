from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from financials.forms import TransactionForm, EditTransactionForm, BudgetForm
from financials.models import Transaction, Category, Account

# Create your views here.
@login_required
def index(request):
    context = {}
    context['title'] = 'Money Parce'

    account, _ = Account.objects.get_or_create(user=request.user)
    account.update_values()
    context['account'] = account
    context['form'] = BudgetForm()
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            account.budget = budget
            account.save()
    context['overbudget'] = account.over_budget()

    return render(request, 'financials/index.html', {'context': context})

@login_required
def transactions_list(request):
    categories = Category.objects.filter(user=request.user)
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
        transactions = Transaction.objects.filter(user=request.user, category__name__in=filter_list, type__in=inout_list)
    else:
        transactions = Transaction.objects.filter(user=request.user, type__in=inout_list)

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
                category = Category(
                    user=request.user,
                    name=form.cleaned_data['new_category'],
                )
                try:
                    category.save()
                    account.category_list.add(category)
                except:
                    category = Category.objects.get(name=form.cleaned_data['new_category'])
            else:
                category = form.cleaned_data['category']
            transaction = Transaction(
                user=request.user,
                amount=form.cleaned_data['amount'],
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
                category = Category(
                    user=request.user,
                    name=form.cleaned_data['new_category'],
                )
                try:
                    category.save()
                    account.category_list.add(category)
                except:
                    category = Category.objects.get(name=form.cleaned_data['new_category'])
            else:
                category = form.cleaned_data['category']

            transaction.amount = form.cleaned_data['amount']
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

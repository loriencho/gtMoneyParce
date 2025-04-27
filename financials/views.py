from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView

from financials.forms import TransactionForm
from financials.models import Transaction, Category, Account, Budget


# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parce'
    return render(request, 'financials/index.html', {'template_data': template_data})

@login_required
def transactions_list(request):
    categories = Category.objects.filter(user=request.user)
    context = {}
    filter_list = []
    inout_list = []
    for category in categories:
        if request.GET.get(category.name):
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
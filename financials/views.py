from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from financials.models import Transaction, Category


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
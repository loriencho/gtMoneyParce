from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from financials.models import Transaction

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parce'
    return render(request, 'financials/index.html', {'template_data': template_data})

@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}
    return render(request, 'financials/transactions-list.html', context)
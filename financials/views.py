from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parce'
    return render(request, 'financials/index.html', {'template_data': template_data})
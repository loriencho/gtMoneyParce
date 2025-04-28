from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Money Parce'
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})

def help(request):
    template_data = {}
    template_data['title'] = 'Help'
    return render(request, 'home/help.html', {'template_data': template_data})
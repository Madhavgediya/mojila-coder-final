from django.shortcuts import render

# Create your views here.

def landing_page(request):
    return render(request, 'landing_page.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def career_advisor_input_page(request):
    return render(request, 'career_advisor_input_page.html')

def acadamic(request):
    return render(request, 'acadamic.html')

def result(request):
    return render(request, 'result.html')

def recommand_course(request):
    return render(request, 'recommander_course.html')

def plans(request):
    return render(request, 'plans.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def chatbot(request):
    return render(request, 'chatbot.html')








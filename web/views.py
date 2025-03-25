from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

# Homepage
def homepage(request):
    return render(request, 'homepage.html')
#login
def login_view(request):
    return render(request, 'login.html')
#contact us 
def contact_view(request):
    # you can Complete the required functions here
    return render(request, 'contact.html') 
# sign up
def signup_view(request):
    return render(request, 'signup.html')





# Info section
def info(request):
    return render(request, 'info/info.html')

def gym_info(request):
    return render(request, 'info/gym_info.html')

def facility_info(request):
    return render(request, 'info/facility_info.html')

def announcement_info(request):
    return render(request, 'info/announcement_info.html')

def cost_info(request):
    return render(request, 'info/cost_info.html')

# Membership management
def membership(request):
    return render(request, 'membership/membership.html')

def renew_membership(request):
    return render(request, 'membership/renew_membership.html')

def cancel_membership(request):
    return render(request, 'membership/cancel_membership.html')

def update_membership(request):
    return render(request, 'membership/update_membership.html')

# Member only
def memberonly(request):
    return render(request, 'memberonly/memberonly.html')

def book_class(request):
    return render(request, 'memberonly/book_class.html')

def book_activity(request):
    return render(request, 'memberonly/book_activity.html')

def feedback(request):
    return render(request, 'memberonly/feedback.html')

# Staff only
def staffonly(request):
    return render(request, 'staffonly/staffonly.html')

def create_class(request):
    return render(request, 'staffonly/create_class.html')

def cancel_class(request):
    return render(request, 'staffonly/cancel_class.html')

def create_announcement(request):
    return render(request, 'staffonly/create_announcement.html')

def staff_feedback(request):
    return render(request, 'staffonly/staff_feedback.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def signup_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username taken!"})
        
        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"success": True})
    
def login_ajax(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
from django.shortcuts import render ,redirect
from .forms import UserRegisterForm , UserLoginForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login ,authenticate ,logout
from users.models import MyUser
import random
# Create your views here.


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            
            if user:
                login(request,user)
                return redirect(request.GET.get("next","profiles:profile"),user)
            else:
                messages.error(request,"Invalid username or password")   
        else:
            pass
    else:
        form = UserLoginForm()
    return render(request,"accounts/login.html",{'form':form})

def register(request):
    form = UserRegisterForm()
    code = random.randint(000000,999999)
    request.session['code'] = code
    email = request.POST.get("email")
    subject = "social media"
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]
            if password != password_confirm:
                messages.error(request,"Password is not match")
            else:
                user.is_active = False
                user.set_password(password_confirm)
                user.save()
                request.session['user_id'] = user.id
                
                send_mail(subject,f"code for register {code}",settings.EMAIL_HOST_USER,[email])
                return redirect("account:verify_code")
        else:
            form = UserRegisterForm()
    return render(request,"accounts/register.html",{'form':form})

def vrify_code(request):
    get_code = request.session.get('code')
    form_code = request.POST.get('verify')
    user_id = request.session.get('user_id')
    
    try:
        user = MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        return redirect("account:register")
    
    if request.method == "POST":
        if str(form_code) == str(get_code):
            user.is_active = True
            user.save()
            login(request,user)
            return redirect("profiles:profile",user)
        else:
            return render(request,"account/verify_code.html")
    else:
        messages.error(request,"form is not valid!!!")
    return render(request,"accounts/verify_code.html")

def logout_user(request):
    logout(request)
    return redirect("account:login")
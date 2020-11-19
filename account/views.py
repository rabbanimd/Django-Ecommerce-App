from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    # else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password1']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                # messages.info(request,'you are now logged in as {username}')
                return redirect('/')
            else:
                messages.error(request, 'invalid username/password...')
                return redirect('/')
        else:
            return render(request, "login.html")
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']
        re_password=request.POST['password2']
        if password==re_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'username alreday exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email alreday exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')
        else:
            messages.warning(request,'Password not Matching......')
            return redirect('register')

    else:
     return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
# Create your views here.

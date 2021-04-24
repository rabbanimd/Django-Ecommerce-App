from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from rest_framework import generics,views
# from .utils import Util
# from rest_framework.views import APIView
from .serializer import ResetPasswordSerializer#resetpasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
def login(request):
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
                return render(request, "login.html")
        else:
            messages.warning(request,"To continue , you must login first ")
            return render(request, "login.html")
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']
        re_password=request.POST['password2']
        if password == re_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'username alreday exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email alreday exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('/')
        else:
            messages.warning(request,'Password not Matching......')
            return redirect('register')
    else:
     return render(request,'register.html')

def Reset_pass_Request_email(request):
        return render(request,"reset_password.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

class ResetPasswordEmailApiView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self,request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site (request=request).domain
            relativeLink = reverse('password-reset-confirm',
                   kwargs={'uidb64':uidb64 , 'token':token})
            absurl = 'http://' + current_site+relativeLink
            data = {'to_mail': user.email}
            # Util.send_email(data)
        return data
        data = {'request': requset,'data': requset.data}
        serializer = self.serializer_class(data)
        serializer.is_valid(raise_exception=True)

class PasswordTokenCheckApi(generics.GenericAPIView):
    def get(self,request,uidb64 ,token):
        pass

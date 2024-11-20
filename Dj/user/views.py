from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth 
from django.utils.timezone import datetime

import pyotp

from .models import User, Profile
from .forms import UserRegister, LoginForm, OTPForm
from .utils import sendToken


############################### TODO : Authentication ###############################


def loginUser(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('HOME')
    elif request.method == 'POST':
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            password = form.cleaned_data.get("password")
            
            user = auth.authenticate(request=request, phone=phone, password=password)
            
            if user is not None:
                sendToken(request=request, phone=phone)
                request.session['phone'] = phone
                return redirect('OTP-LOGIN-VERIFY')
            else:
                print("error1")
                messages.error(request, 'مشخصات وارد شده اشتباه می باشد، دوباره تلاش کنید')
                return redirect("LOGIN")
        else:
            print("error2")
            messages.error(request, "")
            return redirect('LOGIN')
    return render(request, "user/login.html", {'form':form})


def otpLoginValidation(request):
    form = OTPForm(request.POST, None)
    if request.method == 'POST':
        if form.is_valid():
            otp = form.cleaned_data.get("otp")
            phone = request.session["phone"]
            otp_secret_key = request.session["otp_secret_key"]
            otp_valid_until = request.session["otp_valid_date"]
            
            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=180)
                    
                    if totp.verify(otp):
                        user = get_object_or_404(User, phone=phone)
                        
                        auth.login(request=request, user=user)

                        del request.session["otp_secret_key"]
                        del request.session["otp_valid_date"]
                        
                        return redirect('HOME')
                    else:
                        messages.error(request, 'otp is used before or expired')
                        return redirect('OTP-LOGIN-VERIFY')
                else:
                    messages.error(request, 'otp time has passed')
                    return redirect('OTP-LOGIN-VERIFY')
            else:
                messages.error(request, 'the OTP is not acceptable')
                return redirect('LOGIN')
        else:
            messages.error(request, 'the OTP form has problem')
            return redirect('LOGIN')
    form = OTPForm()
    return render(request, 'user/otp_login.html', {'form':form})


def userProfile(request):
    if request.user.is_authenticated:
        user = request.user 
        
        p = Profile.objects.get(user=user)
        
        return render(request, 'user/profile.html', {'profile':p})
    else:
        return redirect('LOGIN')


def logoutUser(request):
    auth.logout(request)
    return redirect('HOME')


################################### TODO : Registration ###################################


def registerUser(request):
    form = UserRegister(request.POST or None)
    if request.user.is_authenticated:
        messages.warning(request, 'شما نمیتوانید به این صفحه مراجعه کنید')
        return redirect('HOME')
    elif request.method == 'POST':
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user = User.objects.create(phone=phone,email=email,password=password,first_name=first_name,
                                       last_name=last_name)
            user.set_password(password)
            user.is_active = False
            user.save()
            request.session["pk"] = user.pk
            sendToken(request=request, phone=phone)
            return redirect('OTP-REGISTER-VERIFY')
        else:
            messages.error(request, f'{form.errors}')
            return redirect('REGISTER')
    else:
        form = UserRegister()
    return render(request, "user/register.html", {'form': form})


def otpRegisterValidation(request):
    form = OTPForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            otp = form.cleaned_data.get("otp")
            pk = request.session["pk"]
            otp_secret_key = request.session["otp_secret_key"]
            otp_valid_until = request.session["otp_valid_date"]
            
            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=180)
                    
                    if totp.verify(otp):
                        print(pk)
                        user = User.objects.get(pk=pk)
                        
                        user.is_active = True
                        
                        user.save()

                        del request.session["otp_secret_key"]
                        del request.session["otp_valid_date"]
                        
                        messages.success(request, '')
                        
                        return redirect('HOME')
                    
                    else:
                        messages.error(request, 'otp is used before or expired')
                        return redirect('OTP-REGISTER-VERIFY')
                else:
                    messages.error(request, 'otp time has passed')
                    return redirect('OTP-REGISTER-VERIFY')
            else:
                messages.error(request, 'the OTP is not acceptable')
                return redirect('REGISTER')
            
        else:
            messages.error(request, '')
            return redirect('REGISTER')
    return render(request, 'user/otp_register.html', {'form':form})


####################### TODO : Reset_Password #######################


def otpPasswordReset(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        if User.objects.filter(phone__exact=phone):
            user = User.objects.get(phone=phone)
            request.session["pk"] = user.pk
            sendToken(request=request, phone=phone)
            messages.success(request, "")
            return redirect('RESET')
        else:
            messages.error(request, "")
            return redirect("FORGET")
    return render(request, "user/forgetPassowrd.html")


def checkOTP(request):
    form = OTPForm(request.POST, None)
    if request.method == 'POST':
        if form.is_valid():
            otp = form.cleaned_data.get("otp")
            otp_secret_key = request.session["otp_secret_key"]
            otp_valid_until = request.session["otp_valid_date"]
            
            if otp_secret_key and otp_valid_until:
                valid_until = datetime.fromisoformat(otp_valid_until)
                
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=180)
                    
                    if totp.verify(otp):
                        messages.success(request, "")

                        del request.session["otp_secret_key"]
                        del request.session["otp_valid_date"]
                        
                        return redirect("CONFIRM")
                    else:
                        messages.error(request, 'otp is used before or expired')
                        return redirect('RESET')
                else:
                    messages.error(request, 'otp time has passed')
                    return redirect('FORGET')
            else:
                messages.error(request, 'the OTP is not acceptable')
                return redirect('FORGET')
        else:
            messages.error(request, "")
            return redirect("FORGET")
    return render(request, "user/otp_reset_password.html", {"form":form})


def confirmResetPassword(request):
    if request.user.is_authenticated:
        messages.warning(request, 'شما نمیتوانید به این صفحه مراجعه کنید')
        return redirect('HOME')
    elif request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password == confirm_password:
            pk = request.session.get("pk")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'گذر واژه با موفقیت بازیابی شد')
            return redirect('LOGIN')
        else:
            messages.error(request, "")
            return redirect("CONFIRM")
    return render(request, "user/confirm_password.html")

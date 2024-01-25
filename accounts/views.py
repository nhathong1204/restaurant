from django.shortcuts import render, redirect
from accounts.forms import UserForm, UserLoginForm, VendorForm
from accounts.utils import detectUser
from .models import User, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #create user using form
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(form.cleaned_data['password'])
            # user.save()
            
            #create user using create_user function
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been created successfully')
            
            redirect('registerUser')
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.role = User.VENDOR
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            vendor = v_form.save(commit=False)
            vendor.user_profile = user_profile
            vendor.user = user
            vendor.save()
            messages.success(request, 'Your account has been registered successfully. Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your are now logged in")
                return redirect('dashboard')
            else:
                messages.warning(request, f"User does not exist. Create an account.")
        except:
            messages.warning(request, f"User with {email} does not exist")
        
    context = {'form': form}
    
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'Your are now logged out.')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
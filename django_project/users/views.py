from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegisterForm, ProfileForm
from .tokens import account_activation_token

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def register(request):
    user_form = UserRegisterForm()
    profile_form = ProfileForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            auth_login(request, user)
            profile_form = ProfileForm(
                request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                message = render_to_string('users/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user_form.cleaned_data.get('username')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                auth_logout(request)
                messages.success(
                    request, f'An email has been sent with instructions to active your account.')
                return redirect('ta_system:home')
            else:
                auth_logout(request)
                userData = User.objects.get(username=username)
                userData.delete()
        else:
            auth_logout(request)
            userData = User.objects.get(username=username)
            userData.delete()
            messages.error(request, f'Please Correct The Error Below.')
    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(
            request, f'Your account has been activate successfully!')
        return redirect('ta_system:home')
    else:
        messages.error('Activation link is invalid!')


def login(request):
    return render(request, 'users/login.html', {'title': 'Login'})

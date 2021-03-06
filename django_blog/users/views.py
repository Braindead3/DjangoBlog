import os
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST,
                                                request.FILES,
                                                instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            upd_user = User.objects.filter(username=request.user.username).first()
            if Path(upd_user.profile.image.path).is_file():
                os.remove(upd_user.profile.image.path)
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Tranlations for dark mode
LIGHT = _('Light')
DARK = _('Dark')


@login_required
def index(request):
    return render(request, 'index.html', {})


def switch(request):
    if request.user and request.user.is_authenticated:
        profile = request.user.profile
        if profile.learn is None:
            return redirect(reverse('userprofile:update'))
        return redirect(reverse('home'))
    return redirect(reverse('account_login'))

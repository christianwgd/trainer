from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

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


@require_POST
def toggle_session_recent(request):
    request.session['recent_only'] = not(request.session.get('recent_only', False))
    return JsonResponse({'result': 1})

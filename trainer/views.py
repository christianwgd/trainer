# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


# Tranlations for dark mode
LIGHT = _('Light')
DARK = _('Dark')


@login_required
def index(request):
    return render(request, 'index.html', {})

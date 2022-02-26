from django.shortcuts import redirect

import requests


def welcome(request):
    return redirect('accounts:login')
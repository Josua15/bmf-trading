from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BmfBtcUsdtDaily 
import openpyxl  
from .controllers.home import home_view_logic


# Create your views here.

def home_view(request):
    response = home_view_logic(request)
    if response:
        return response 

    
    context = {
        'page_title': 'Console Home',
        'message': 'Console',
        'cta_text': 'Upload your Excel files and process the data.',
        'upload_button': 'Upload Excel Doc'
    }
    return render(request, 'home.html', context)



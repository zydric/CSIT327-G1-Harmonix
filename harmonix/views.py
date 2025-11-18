from django.shortcuts import render

def landing_page(request):
    """Landing page for unauthenticated users - shows login/register options"""
    return render(request, 'landing.html')

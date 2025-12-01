from django.shortcuts import render, redirect

def landing_page(request):
    """Landing page for guests; authenticated users jump to their hub."""
    if request.user.is_authenticated:
        if request.user.is_musician:
            return redirect('musician_dashboard')
        if request.user.is_band_admin:
            return redirect('listings:feed')
        return redirect('listings:feed')

    return render(request, 'landing.html')

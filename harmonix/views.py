from django.shortcuts import render, redirect


def landing_page(request):
    """Landing page for guests; authenticated users jump to their hub."""
    if request.user.is_authenticated:
        if request.user.is_musician:
            return redirect('musician_dashboard')
        if request.user.is_band_admin:
            return redirect('band_admin_dashboard')
        return redirect('listings:feed')

    return render(request, 'landing.html')


# ============================
# Custom Error Handlers
# ============================

def handler400(request, exception=None):
    """Custom 400 Bad Request handler."""
    return render(request, 'errors/400.html', status=400)


def handler403(request, exception=None):
    """Custom 403 Forbidden handler."""
    return render(request, 'errors/403.html', status=403)


def handler404(request, exception=None):
    """Custom 404 Not Found handler."""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Custom 500 Internal Server Error handler."""
    return render(request, 'errors/500.html', status=500)

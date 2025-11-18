from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Application
from listings.models import Listing


@login_required
def apply_to_listing(request, pk):
    """
    Handle musician applications to band listings
    """
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    
    # Only musicians can apply
    if not request.user.is_musician:
        messages.error(request, "Only musicians can apply to listings.")
        return redirect('listings:detail', pk=listing.pk)
    
    # Check if already applied
    if listing.is_applied_by(request.user):
        messages.warning(request, "You have already applied to this listing.")
        return redirect('listings:detail', pk=listing.pk)
    
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        
        # Create the application
        Application.objects.create(
            musician=request.user,
            listing=listing,
            message=message
        )
        
        messages.success(request, f"Your application to '{listing.title}' has been submitted!")
        return redirect('listings:detail', pk=listing.pk)
    
    # GET request - redirect to listing detail (applications are handled via modal)
    return redirect('listings:detail', pk=listing.pk)


@login_required
def update_application_status(request, pk):
    """
    Update application status (accept/reject) - only for band admins
    """
    application = get_object_or_404(Application, pk=pk)
    
    # Check if user is the band admin who owns this listing
    if request.user != application.listing.band_admin:
        return HttpResponseForbidden("You can only manage applications to your own listings.")
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['accepted', 'rejected']:
            old_status = application.get_status_display()
            application.status = new_status
            application.save()
            
            status_display = application.get_status_display()
            messages.success(
                request, 
                f"Application from {application.musician.username} has been {status_display.lower()}."
            )
        else:
            messages.error(request, "Invalid status provided.")
    
    return redirect('listings:detail', pk=application.listing.pk)


@login_required
def withdraw_application(request, pk):
    """
    Allow musicians to withdraw their pending applications
    """
    application = get_object_or_404(Application, pk=pk)
    
    # Check if user owns this application
    if request.user != application.musician:
        return HttpResponseForbidden("You can only withdraw your own applications.")
    
    # Only pending applications can be withdrawn
    if application.status != 'pending':
        messages.error(request, "Only pending applications can be withdrawn.")
        return redirect('applications:my_applications')
    
    if request.method == 'POST':
        listing_title = application.listing.title
        application.delete()
        messages.success(request, f"Your application to '{listing_title}' has been withdrawn.")
        return redirect('applications:my_applications')
    
    # If not POST, redirect back
    return redirect('applications:my_applications')


@login_required 
def my_applications(request):
    """
    Show musician's applications or band admin's received applications
    """
    if request.user.is_musician:
        # Show applications made by this musician
        applications = Application.objects.filter(musician=request.user).order_by('-created_at')
        context = {
            'applications': applications,
            'user': request.user,
        }
        return render(request, 'applications/my_applications.html', context)
    else:
        # Show applications to this band's listings
        applications = Application.objects.filter(listing__band_admin=request.user).order_by('-created_at')
        context = {
            'applications': applications,
            'user': request.user,
        }
        return render(request, 'applications/received_applications.html', context)
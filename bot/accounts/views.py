from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from .models import CustomUser
from .forms import UserRegistrationForm, UserProfileForm  # You'll need to create these forms

@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful! Welcome to our platform.'))
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, _('Welcome back!'))
            return redirect('home')
        else:
            messages.error(request, _('Invalid email or password.'))
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, _('You have been logged out successfully.'))
    return redirect('login')

@login_required
def profile_view(request):
    """Display and update user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_profile_image(request):
    """Handle profile image updates via AJAX"""
    if not request.FILES.get('profile_image'):
        return JsonResponse({'error': _('No image file provided')}, status=400)
        
    try:
        request.user.update_profile_image(request.FILES['profile_image'])
        return JsonResponse({
            'success': True,
            'image_url': request.user.get_profile_image_url()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def delete_account(request):
    """Handle account deletion"""
    if request.method == 'POST':
        try:
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, _('Your account has been deleted successfully.'))
            return redirect('home')
        except Exception as e:
            messages.error(request, _('Failed to delete account. Please try again.'))
            return redirect('profile')
    
    return render(request, 'accounts/delete_account.html')

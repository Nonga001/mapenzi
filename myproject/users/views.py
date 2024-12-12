from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from .models import Announcement
from .forms import AnnouncementForm  # assuming you have a form to handle announcements

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = None  # Set role to None explicitly
            user.save()
            return redirect('login')  # Redirect to login or any other page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to the dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def home(request):
    # You can pass any context to the template if needed
    context = {
        'user': request.user,  # You can pass the logged-in user data to the template
    }
    return render(request, 'home.html', context)

def profile(request):
    # You can pass the user details or other context to the template
    context = {
        'user': request.user,
    }
    return render(request, 'profile.html', context)

def enrollment(request):
    # Example view for enrollment
    context = {
        'user': request.user,
    }
    return render(request, 'enrollment.html', context)

def course(request):
    # Example view for course
    context = {
        'user': request.user,
    }
    return render(request, 'course.html', context)

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name='lecturers').exists():
        role = "lecturer"
        functions = [
            "View Announcements",
            "Create Announcement",
            "Edit Announcement",
            "Delete Your Announcement",
        ]
    elif user.groups.filter(name='students').exists():
        role = "student"
        functions = ["View Announcements"]
    else:
        role = None
        functions = []

    context = {
        'role': role,
        'functions': functions,
    }
    return render(request, 'home.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to the dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def home(request):
    # You can pass any context to the template if needed
    context = {
        'user': request.user,  # You can pass the logged-in user data to the template
    }
    return render(request, 'home.html', context)


@login_required
def profile(request):
    user = request.user
    # Get all the group names the user is a part of
    groups = user.groups.values_list('name', flat=True)

    # Debugging: Print the groups the user belongs to
    print(groups)

    # Set role based on the group the user belongs to
    if 'lecturers' in groups:  # Match the exact group name from the admin panel (in lowercase)
        role = 'Lecturer'
    elif 'students' in groups:
        role = 'Student'
    else:
        role = 'Unknown'  # If no specific group is found, set as Unknown

    context = {
        'role': role,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    return render(request, 'profile.html', context)
def enrollment(request):
    # Example view for enrollment
    context = {
        'user': request.user,
    }
    return render(request, 'enrollment.html', context)

def course(request):
    # Example view for course
    context = {
        'user': request.user,
    }
    return render(request, 'course.html', context)

@login_required
def home(request):
    user = request.user
    if user.groups.filter(name='lecturers').exists():
        role = "lecturer"
        functions = [
            "View Announcements",
            "Create Announcement",
            "Edit Announcement",
            "Delete Your Announcement",
        ]
    elif user.groups.filter(name='students').exists():
        role = "student"
        functions = ["View Announcements"]
    else:
        role = None
        functions = []

    # Get all announcements, ordered by most recent
    announcements = Announcement.objects.all().order_by('-created_at')

    context = {
        'role': role,
        'functions': functions,
        'announcements': announcements,
    }

    return render(request, 'home.html', context)

@login_required
def create_announcement(request):
    if request.user.groups.filter(name='lecturers').exists():  # Check if user is a lecturer
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.creator = request.user  # Assign the logged-in user as the creator
                announcement.save()
                return redirect('home')  # Redirect to the home page after saving the announcement
        else:
            form = AnnouncementForm()

        return render(request, 'create_announcement.html', {'form': form})
    else:
        return redirect('home')  # If not a lecturer, redirect to the home page

@login_required
@login_required
def edit_announcement(request, id):
    # Get the announcement by ID or 404 if not found
    announcement = get_object_or_404(Announcement, id=id)

    # Check if the user is the creator of the announcement or has permission to edit
    if announcement.creator != request.user:
        return redirect('home')  # Or you can show a message if you want

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect after successful save
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})

@login_required
def delete_announcement(request, id):
    # Get the announcement by ID or return 404 if not found
    announcement = get_object_or_404(Announcement, id=id)

    # Check if the user is the creator of the announcement or has permission to delete
    if announcement.creator != request.user:
        return redirect('home')  # Or you can show a message if you want

    if request.method == 'POST':  # Confirm deletion via POST method
        announcement.delete()
        return redirect('home')  # Redirect to home after deletion

    return render(request, 'confirm_delete.html', {'announcement': announcement})
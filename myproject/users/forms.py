from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Announcement


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Exclude 'role'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = None  # Ensure role is None initially
        if commit:
            user.save()
        return user


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']  # Only allow input for title and content

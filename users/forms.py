from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from books.models import Book
from .models import ReadingChallenge

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'profile_picture']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "profile_picture"]


class AddBookToChallengeForm(forms.ModelForm):
    class Meta:
        model = ReadingChallenge  # ✅ Specify the model
        fields = ['goal', 'end_date']  # ✅ Include fields for user input

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Ensure user is valid before filtering challenges
        if hasattr(user, 'id'):
            self.fields['challenge'] = forms.ModelChoiceField(
                queryset=ReadingChallenge.objects.filter(user=user),
                empty_label="Select a Challenge",
                widget=forms.Select(attrs={'class': 'form-control'})
            )


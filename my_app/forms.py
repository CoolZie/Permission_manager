from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee

class EmployeeRegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    full_name = forms.CharField(
        max_length=255,
        label="Nom complet",
        help_text="Nom complet",
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Genre",
        help_text="",
    )
    department = forms.CharField(
        max_length=100,
        label="Département",
        help_text="",
    )
    position = forms.CharField(
        max_length=100,
        label="Poste",
        help_text="",
    )
    hire_date = forms.DateField(
        label="Date d'embauche",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="",
    )
    phone_no = forms.CharField(
        label='Numéro de téléphone',
        widget=forms.TextInput(
            attrs={
                'pattern': r'\+225[\d]{10}',
                'placeholder': '+225XXXXXXXXXX(Numéro de téléphone)',
            }
        )
    )
    email = forms.EmailField(
        label="Adresse e-mail",
        help_text="",
    )
    photo = forms.ImageField(
        required=False,
        label="Photo",
        help_text="",
    )
    is_admin = forms.BooleanField(
        required=False,
        label="Administrateur",
        help_text="",
    )

    username = forms.CharField(
        label="Nom d'utilisateur",
        help_text="",
    )
    password1 = forms.CharField(
        label="Mot de passe",
        help_text="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'})
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        help_text="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre mot de passe'})
    )


    class Meta:
        model = Employee
        fields = ('username', 'full_name', 'gender', 'department', 'position', 'hire_date', 'phone_no', 'email', 'photo', 'is_admin')



class EmployeeLoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom d\'utilisateur'}))
    password = forms.CharField(label="Mot de passe",widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}))



from .models import PermissionRequest

class PermissionRequestForm(forms.ModelForm):
    class Meta:
        model = PermissionRequest
        fields = ('start_date', 'end_date', 'reason')
        labels = {
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'reason': 'Motif',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
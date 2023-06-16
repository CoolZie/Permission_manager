from django.shortcuts import render, redirect
from .forms import EmployeeRegistrationForm, EmployeeLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PermissionRequestForm
from django.db.models import Count

def home_view(request):
    context = {}
    return render(request, 'my_app/home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription réussie !')
            
            return redirect('my_app:login')  # Rediriger vers la page de connexion après l'inscription
    else:
        form = EmployeeRegistrationForm()
    
        # Traitement des erreurs de validation
    form_errors = form.errors if request.method == 'POST' else None

    context = {
        'form': form,
        'form_errors': form_errors,
    }
    return render(request, 'my_app/register.html', context)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Connexion réussie
                return redirect('my_app:dashboard')
            else:
                # Échec de la connexion
                form.add_error(None, 'Nom d\'utilisateur ou mot de passe incorrect')
    else:
        form = EmployeeLoginForm()

    return render(request, 'my_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('my_app:home') # Rediriger vers la page d'accueil après la déconnexion


@login_required
def dashboard_view(request):
    if request.user.is_admin:
        permission_requests = PermissionRequest.objects.all()
        context = {
            'permission_requests': permission_requests
        }
        return render(request, 'my_app/admin_dashboard.html', context)
    


    else:     
        user = request.user  # Obtient l'utilisateur connecté
        context = {
            'user': user
        }
        return render(request, 'my_app/dashboard.html', context)


from django.core.exceptions import ValidationError

def permission_request_view(request):
    if request.method == 'POST':
        form = PermissionRequestForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            if end_date <= start_date:
                form.add_error('end_date', 'La date de fin doit être supérieure à la date de début.')
            else:
                permission_request = form.save(commit=False)
                permission_request.employee = request.user
                permission_request.save()
                messages.success(request, 'Demande de permission envoyée !')
                return redirect('my_app:dashboard')
    else:
        form = PermissionRequestForm()
    
    context = {
        'form': form,
    }
    return render(request, 'my_app/permission_request.html', context)


@login_required
def history_view(request):  
    user = request.user
    permission_requests = user.permissionrequest_set.all()
    context = {
        'permission_requests': permission_requests
    }
    return render(request, 'my_app/history.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from my_app.models import PermissionRequest
from my_app.forms import PermissionRequestForm
from django.core.exceptions import ValidationError


# Vue pour la modification d'une demande de permission




@login_required
def edit_permission_view(request, pk):
    error_message = ''
    permission = get_object_or_404(PermissionRequest, pk=pk)

    if request.method == 'POST':
        form = PermissionRequestForm(request.POST, instance=permission)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            if end_date <= start_date:
                form.add_error('end_date', 'La date de fin doit être supérieure à la date de début.')
                error_message = "La date de fin doit être supérieure à la date de début."
            else:
                form.save()
                messages.success(request, 'Demande de permission modifiée avec succès.')
                return redirect('my_app:history')
    else:
        form = PermissionRequestForm(instance=permission)

    context = {
        'form': form,
        'permission': permission,
        "error_message": error_message,
    }
    return render(request, 'my_app/edit_permission.html', context)


# Vue pour la suppression d'une demande de permission
@login_required
def delete_permission_view(request, pk):
    permission = get_object_or_404(PermissionRequest, pk=pk)

    if request.method == 'POST':
        permission.delete()
        return redirect('my_app:history')

    context = {
        'permission': permission,
    }
    return render(request, 'my_app/delete_permission.html', context)


@login_required
def permission_list_view(request):
    if not request.user.is_admin:
        return redirect('my_app:dashboard')
    
    permission_requests = PermissionRequest.objects.all()
    context = {
        'permission_requests': permission_requests
    }
    return render(request, 'my_app/permission_list.html', context)


@login_required
def approve_permission_view(request, pk):
    permission = get_object_or_404(PermissionRequest, pk=pk)
    permission.demand_status = 'Approuvée'
    permission.is_approved = True
    permission.save()
    return redirect('my_app:permission_list')

@login_required
def reject_permission_view(request, pk):
    permission = get_object_or_404(PermissionRequest, pk=pk)
    permission.demand_status = 'Refusée'
    permission.is_approved = False
    permission.save()
    return redirect('my_app:permission_list')



import json
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from my_app.models import Employee, PermissionRequest

@login_required
def viz_view(request):
    # Nombre total d'employés
 


    # Nombre d'employés non-admin
    non_admin_count = Employee.objects.filter(is_admin=False).count()

    # Nombre de femmes
    female_count = Employee.objects.filter(gender='F').count()

    # Nombre d'hommes
    male_count = Employee.objects.filter(gender='M').count()


    context = {
        'total_employees': json.dumps(non_admin_count) ,
        "total_male": json.dumps(male_count),
        'total_female': json.dumps(female_count),

    }

    return render(request, 'my_app/viz.html', context)

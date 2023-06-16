from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    full_name = models.CharField(max_length=255, verbose_name="Nom complet")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    department = models.CharField(max_length=100, verbose_name="Département")
    position = models.CharField(max_length=100, verbose_name="Poste")
    hire_date = models.DateField(verbose_name="Date d'embauche")
    phone_no = models.IntegerField(null=True, verbose_name="Numéro de téléphone")
    email = models.EmailField(verbose_name="Adresse e-mail")
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True, verbose_name="Photo")
    is_admin = models.BooleanField(default=False, verbose_name="Administrateur")
    

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='employee_groups',
        related_query_name='employee',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='employee_user_permissions',
        related_query_name='employee',
        help_text='Permissions for the employee',
    )

    def __str__(self):
        return self.full_name



class PermissionRequest(models.Model):
    STATUS_CHOICES = [
        ("en_verification", "En vérification"),
        ("approuvee", "Approuvée"),
        ("rejetee", "Rejetée"),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    reason = models.TextField(verbose_name="Motif")
    demand_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    demand_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="en_verification",
        verbose_name="Statut de la demande"
    )
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")

    def __str__(self):
        return f"Permission #{self.id} - {self.employee.username}"

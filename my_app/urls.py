from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'my_app'
urlpatterns = [
    path("", views.home_view, name="home"),  # url page d'acceuil
    path("register/", views.register_view, name="register"),  # url d'inscription
    path("login/", views.login_view, name="login"),  # url de connexion
    path("dashboard/", views.dashboard_view, name="dashboard"),  # url du tableau de bord*
    path('logout/', views.logout_view, name='logout'),  # url de déconnexion
    path('permission_request/', views.permission_request_view, name='permission_request'),  # url de demande de permission
    path("history/", views.history_view, name="history"),  # url de l'historique
    path('permission/<int:pk>/edit/', views.edit_permission_view, name='edit_permission'), # url de modification de permission
    path('permission/<int:pk>/delete/', views.delete_permission_view, name='delete_permission'), # url de suppression de permission
    path('permission-list/', views.permission_list_view, name='permission_list'), # url de la liste des permissions
    path('permission/approve/<int:pk>/', views.approve_permission_view, name='approve_permission'), # url d'approbation de permission
    path('permission/reject/<int:pk>/', views.reject_permission_view, name='reject_permission'), # url de rejet de permission
    path('viz/', views.viz_view, name='visualisation'), # url des visuels
]
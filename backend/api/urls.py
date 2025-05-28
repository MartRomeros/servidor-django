from django.urls import path
from .views import exportar_archivo

urlpatterns = [
    path('exportar/',exportar_archivo),
]
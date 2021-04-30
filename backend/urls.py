from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('uploadImg/', views.uploadImg),
    path('Formula_Recognition/', views.Formula_Recognition),

]

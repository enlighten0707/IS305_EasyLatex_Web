from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('sketchProcess/', views.sketchProcess),
    path('colorization/', views.colorization),
    # path('expr/', views.expr),
    path('XunFeiAPI/', views.XunFeiAPI),

]

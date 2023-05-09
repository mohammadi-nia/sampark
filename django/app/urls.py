from django.urls import path, include
from app import views

urlpatterns = [
    path('get_parking_full_spaces_number/', views.get_parking_full_spaces_number),
    path('create_ticket/', views.create_ticket),
    path('delete_ticket/<int:pk>/', views.delete_ticket),
    path('search/', views.search),
]

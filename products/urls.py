from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products, name='get_products'),
    path('categories/', views.get_categories, name='get_categories'),
    path('retailers/', views.get_retailers, name='get_retailers'),
    path('search/', views.search_products, name='search_products'),
    path('compare/<str:product_name>/', views.compare_prices, name='compare_prices'),
    path('<int:product_id>/', views.get_product_details, name='get_product_details'),
]
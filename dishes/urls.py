from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('', views.DishListView.as_view(), name='index'),
    path('<int:pk>/', views.DishSingleView.as_view(), name='single_dish'),
    path('create-order/<int:dish_id>', views.create_order, name='create_order'),
    path('not-found-404/', views.not_found, name='not_found')
]

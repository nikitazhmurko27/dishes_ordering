from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'dishes'

urlpatterns = [
    path('',
         cache_page(60)(views.HomepageView.as_view()),
         name='index'),
    path('dishes/',
         cache_page(60, cache='db_cache')(views.DishListView.as_view()),
         name='dishes_list'),
    path('dishes/<int:pk>/',
         cache_page(60, cache='db_cache')(views.DishSingleView.as_view()),
         name='single_dish'),
    path('orders/', views.OrderListView.as_view(), name='orders_list'),
    path('create-order/<int:dish_id>', views.CreateOrderView.as_view(), name='create_order'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration')
]

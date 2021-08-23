from django.urls import path, include
from rest_framework import routers
from api.views import DishList, \
                      DishDetail, \
                      IngredientList, \
                      DishTopList

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('dishes/',
         DishList.as_view(),
         name='dishes-list'),
    path('dishes/<int:pk>/',
         DishDetail.as_view(),
         name='dishes-single'),
    path('ingredients/',
         IngredientList.as_view(),
         name='ingredients-list'),
    path('dishes/top',
         DishTopList.as_view(),
         name='dishes-top'),
]

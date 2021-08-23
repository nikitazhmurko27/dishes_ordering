from dishes.models import Dish, \
                          DishIngredients, \
                          Ingredient, \
                          Order
from django.db.models import Count
from rest_framework import generics, mixins
from api.serializers import DishSerializer, \
                            IngredientSerializer, \
                            DishTopSerializer
import logging
logger = logging.getLogger(__name__)


class DishList(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class IngredientList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DishTopList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    top_count = 3
    queryset = Dish.objects \
                   .all() \
                   .annotate(orders_count=Count('order')) \
                   .order_by('-orders_count')[:top_count]
    logger.debug(queryset)

    serializer_class = DishTopSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


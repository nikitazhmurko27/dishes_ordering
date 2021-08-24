from dishes.models import Dish, \
                          DishIngredients, \
                          Ingredient, \
                          Order
from django.db.models import Count
from rest_framework import generics, mixins, filters
from api.serializers import DishSerializer, \
                            IngredientSerializer, \
                            DishTopSerializer
from api.permissions import IsActiveUser
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import DishesFilter
import logging
logger = logging.getLogger(__name__)


class DishList(generics.ListCreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DishesFilter
    ordering_fields = ['created_at']
    ordering = ['created_at']


class DishDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsActiveUser]


class IngredientList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsActiveUser]

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
    permission_classes = [IsActiveUser]
    logger.debug(queryset)

    serializer_class = DishTopSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


from rest_framework import serializers
from dishes.models import Dish, DishIngredients, Ingredient, Order
import logging

logger = logging.getLogger(__name__)


class DishIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = DishIngredients
        fields = ['ingredient', 'name', 'amount']


class DishSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="iso-8601",
                                           read_only=True)
    ingredients = DishIngredientsSerializer(many=True,
                                            source='dish_ingredients')

    class Meta:
        model = Dish
        fields = ['id', 'name', 'ingredients', 'created_at']

    def create(self, validated_data):
        logger.debug(validated_data)
        ingredients_data = validated_data.pop('dish_ingredients')
        dish = Dish.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            DishIngredients.objects.create(dish=dish,
                                           **ingredient_data)
        return dish

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        ingredients_data = validated_data.pop('dish_ingredients')
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data.get('ingredient')
            if ingredient:
                ingredient_item = \
                    DishIngredients.objects.get(ingredient=ingredient,
                                                dish=instance)
                ingredient_item.amount = \
                    ingredient_data.get('amount',
                                        ingredient_item.amount)
                ingredient_item.save()
            else:
                DishIngredients.objects.create(dish=instance,
                                               **ingredient_data)
        return instance


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class DishTopSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dish
        fields = ['id', 'name', 'orders_count']

from django.db import models
from django.core.validators import MinValueValidator


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    ingredients = models.ManyToManyField('Ingredient', through='DishIngredients')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_ingredients_list(self):
        ingredients = []
        for ingredient in self.dish_ingredients.select_related():
            ing_dict = {
                'ingredient': ingredient.ingredient,
                'amount': ingredient.amount,
            }
            ingredients.append(ing_dict)
        return ingredients


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = models.ManyToManyField('Ingredient', through='OrderIngredients')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.order_id)


class DishIngredients(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dish_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


class OrderIngredients(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

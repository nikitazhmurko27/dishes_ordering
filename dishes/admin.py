from django.contrib import admin
from .models import Dish
from .models import Ingredient
from .models import Order


class DishIngredientsInline(admin.TabularInline):
    model = Dish.ingredients.through


class OrderIngredientsInline(admin.TabularInline):
    model = Order.ingredients.through


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [
        DishIngredientsInline,
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'created_at')
    inlines = [
        OrderIngredientsInline,
    ]


admin.site.register(Dish, DishAdmin)
admin.site.register(Ingredient)
admin.site.register(Order, OrderAdmin)

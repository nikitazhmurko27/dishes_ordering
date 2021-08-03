from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Dish, Order, Ingredient, OrderIngredients, DishIngredients
from django.forms import modelformset_factory, ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class DishesListView(ListView):
    model = Dish
    template_name = 'dish/index.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        return Dish.objects.all()
        # return Dish.objects.prefetch_related(
        #     'dish_ingredients',
        #     'dish_ingredients__ingredient'
        # )


class DishSingleView(DetailView):
    model = Dish
    template_name = 'dish/single-dish.html'
    context_object_name = 'dish'


class OrderForm(ModelForm):
    class Meta:
        model = OrderIngredients
        fields = ('ingredient', 'amount')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        min_amount = 1
        if amount < min_amount:
            raise ValidationError(f'The amount should not be less than {min_amount}')
        return amount


def create_order(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('dishes:not_found'))
    initial_values = dish.get_ingredients_list()
    OrderFormSet = modelformset_factory(OrderIngredients, form=OrderForm, can_delete=False, extra=len(initial_values))
    formset = OrderFormSet(initial=initial_values, queryset=OrderIngredients.objects.none().select_related())
    if request.method == 'GET':
        context = {'form': formset}
        return render(request, 'order/create-order.html', context)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST)
        if not formset.is_valid():
            context = {'form': formset}
            return render(request, 'order/create-order.html', context)
        order = Order()
        order.save()
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order = order
            instance.save()
        formset.save_m2m()
        return HttpResponseRedirect(reverse('dishes:index'))


def not_found(request):
    return render(request, 'dish/404.html')

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Dish, Order, OrderIngredients
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderForm, DishFilterForm
from django.views import View


class DishListView (View):
    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.all()

        filter_form = DishFilterForm(request.GET)
        if filter_form.is_valid():
            search_str = filter_form.cleaned_data.get("search_str")
            date_from = filter_form.cleaned_data.get("date_from")
            date_to = filter_form.cleaned_data.get("date_to")
            order_by = filter_form.cleaned_data.get("order_by")

            if search_str:
                dishes = dishes.filter(name__icontains=f'{search_str}')
            if date_from:
                dishes = dishes.filter(created_at__gte=f'{date_from}')
            if date_to:
                dishes = dishes.filter(created_at__lte=f'{date_to}')
            if order_by == 'ASC':
                dishes = dishes.order_by('created_at')

        context = {
            'dishes': dishes,
            'filter': filter_form,
        }

        return render(
            request,
            'dish/index.html',
            context
        )


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

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Dish, Order, OrderIngredients
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderForm, DishFilterForm
from django.views import View
import logging


logger = logging.getLogger(__name__)


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'dish/index.html',
        )


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
            'dish/dish-list.html',
            context
        )


class DishSingleView(DetailView):
    model = Dish
    template_name = 'dish/single-dish.html'
    context_object_name = 'dish'


class OrderListView(ListView):
    model = Order
    template_name = 'order/orders-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.prefetch_related(
            'order_ingredients',
            'order_ingredients__ingredient'
        )


class CreateOrderView(View):
    def get(self, request, dish_id):
        dish = get_object_or_404(Dish, id=dish_id)
        initial_values = dish.get_ingredients_list()
        OrderFormSet = modelformset_factory(OrderIngredients,
                                            form=OrderForm,
                                            can_delete=False,
                                            extra=len(initial_values)
                                            )
        formset = OrderFormSet(initial=initial_values,
                               queryset=OrderIngredients.objects.none().select_related()
                               )
        context = {'form': formset, 'dish_name': dish.name}
        return render(request, 'order/create-order.html', context)

    def post(self, request, dish_id):
        logger.info('creating order start')
        dish = get_object_or_404(Dish, id=dish_id)
        initial_values = dish.get_ingredients_list()
        OrderFormSet = modelformset_factory(OrderIngredients,
                                            form=OrderForm,
                                            can_delete=False,
                                            extra=len(initial_values)
                                            )
        formset = OrderFormSet(request.POST)
        logger.debug(request.POST)
        if not formset.is_valid():
            logger.error('order form is invalid')
            context = {'form': formset}
            return render(request, 'order/create-order.html', context)
        order = Order()
        order.save()
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order = order
            instance.save()
        formset.save_m2m()
        logger.info('order added successfully')
        return HttpResponseRedirect(reverse('dishes:orders_list'))

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Dish, Order, OrderIngredients
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import OrderForm, DishFilterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.views import View
import logging
from datetime import datetime, date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request,
            'login.html',
            {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dishes:index'))
        return render(
            request,
            'login.html',
            {
                'form': form,
                'login_error': 'Invalid username or password'
            }
        )


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(
            request,
            'registration.html',
            {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dishes:index'))
        return render(
            request,
            'registration.html',
            {'form': form}
        )


class LogoutView(LoginRequiredMixin, View):
    login_url = '/dishes-ordering/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('dishes:index'))


class HomepageView(LoginRequiredMixin, View):
    login_url = '/dishes-ordering/login/'

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'dish/index.html',
        )


class DishListView (LoginRequiredMixin, View):
    login_url = '/dishes-ordering/login/'

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


class DishSingleView(LoginRequiredMixin, DetailView):
    login_url = '/dishes-ordering/login/'

    model = Dish
    template_name = 'dish/single-dish.html'
    context_object_name = 'dish'


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/dishes-ordering/login/'

    model = Order
    template_name = 'order/orders-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user).prefetch_related(
            'order_ingredients',
            'order_ingredients__ingredient'
        )


def get_ingredient_diff(dish_ingredients, order_ingredients):
    """
    Get the difference ingredients between dish and order
    :param dish_ingredients:
    :param order_ingredients:
    :return: list
    """
    pairs = zip(dish_ingredients, order_ingredients)
    diffs = []
    for x, y in pairs:
        if x == y:
            continue
        for k in x:
            if x[k] == y[k]:
                continue
            diffs.append({
                'name': x['ingredient'].name,
                'current': y[k],
            })
    return diffs


def get_daily_orders():
    """
    Collect data orders from last day
    :return:
    """
    today = date.today()
    midnight = datetime.combine(today, datetime.min.time())
    orders = Order.objects.filter(created_at__gte=midnight)

    data = []
    for order in orders:
        dish_ingredients = order.dish.get_ingredients_list()
        order_ingredients = order.get_ingredients_list()
        diffs = get_ingredient_diff(dish_ingredients,
                                    order_ingredients)
        diffs_str = ""
        for ingredient_diff in diffs:
            diff_str = f"{ingredient_diff['name']} " \
                       f"- {ingredient_diff['current']};"
            diffs_str += diff_str
        is_change = True
        if len(diffs) == 0:
            is_change = False
        data.append([order.dish.name, is_change, diffs_str])
    return data


class CreateOrderView(LoginRequiredMixin, View):
    login_url = '/dishes-ordering/login/'

    def get(self, request, dish_id):
        dish = get_object_or_404(Dish, id=dish_id)
        initial_values = dish.get_ingredients_list()
        OrderFormSet = modelformset_factory(OrderIngredients,
                                            form=OrderForm,
                                            can_delete=False,
                                            extra=len(initial_values)
                                            )
        formset = OrderFormSet(
            initial=initial_values,
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
        order = Order(dish=dish, user=request.user)
        order.save()
        instances = formset.save(commit=False)
        for instance in instances:
            instance.order = order
            instance.save()
        formset.save_m2m()
        logger.info('order added successfully')
        return HttpResponseRedirect(reverse('dishes:orders_list'))

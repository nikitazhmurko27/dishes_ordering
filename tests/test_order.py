import pytest
from dishes.models import Dish, Ingredient, DishIngredients
from dishes.views import Order, OrderListView

TEST_DISH_NAME = 'TestDish'
TEST_ING_NAME1 = 'TestIngredient1'
TEST_ING_NAME2 = 'TestIngredient2'


@pytest.fixture
def dish():
    d = Dish.objects.create(name=TEST_DISH_NAME)
    return d


@pytest.fixture
def ing1():
    ing = Ingredient.objects.create(name=TEST_ING_NAME1)
    return ing


@pytest.fixture
def ing2():
    ing = Ingredient.objects.create(name=TEST_ING_NAME2)
    return ing


@pytest.mark.django_db
def test_success_rf(rf):
    request = rf.get('/dishes-ordering/orders', follow=True)
    response = OrderListView.as_view()(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_formset_is_valid(client, dish, ing1, ing2):
    ingredient_amount = 2
    data = {
        "form-TOTAL_FORMS": ingredient_amount,
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": ingredient_amount,
        "form-0-ingredient": ing1.id,
        "form-0-amount": '1',
        "form-1-ingredient": ing2.id,
        "form-1-amount": '2',
    }
    resp = client.post(f"/dishes-ordering/create-order/{dish.id}", data=data)
    assert resp.status_code == 302
    assert Order.objects.all().count() == 1
    assert Order.objects.first().ingredients.count() == ingredient_amount


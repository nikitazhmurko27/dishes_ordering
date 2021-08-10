import pytest
from dishes.models import Dish, Ingredient, DishIngredients
from dishes.views import DishListView, DishSingleView
from unittest import mock

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
def test_dish_str(dish):
    assert str(dish) == TEST_DISH_NAME


@pytest.mark.django_db
def test_dish_ingredients_list(dish, ing1, ing2):
    DishIngredients.objects.create(dish=dish, ingredient=ing1, amount=1)
    DishIngredients.objects.create(dish=dish, ingredient=ing2, amount=2)

    dish_ingredients_list = [
        {
            'ingredient': ing1,
            'amount': 1,
        },
        {
            'ingredient': ing2,
            'amount': 2,
        },
    ]
    with mock.patch('dishes.models.Dish.get_ingredients_list', return_value=dish_ingredients_list):
        assert dish.get_ingredients_list() == dish_ingredients_list


@pytest.mark.django_db
def test_success_dish_list_rf(rf):
    request = rf.get('/dishes-ordering/dishes', follow=True)
    response = DishListView.as_view()(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_exist_single_dish(client, dish):
    resp = client.get(f"/dishes-ordering/dish/{dish.id}", follow=True)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_not_exist_single_dish(client):
    resp = client.get('/dishes-ordering/dish/1', follow=True)
    assert resp.status_code == 404


@pytest.mark.django_db
def test_correct_search(dish, client):
    resp = client.get("/dishes-ordering/dishes/?search_str=Test", follow=True)
    assert resp.status_code == 200
    assert resp.context["dishes"].count() == 1
    assert resp.context["dishes"][0].pk == dish.pk


@pytest.mark.django_db
def test_incorrect_search(client):
    resp = client.get("/dishes-ordering/dishes/?search_str=blablabla", follow=True)
    assert resp.status_code == 200
    assert resp.context["dishes"].count() == 0

import pytest
from dishes.models import Ingredient

TEST_INGREDIENT_NAME = 'TestIngredient'


@pytest.mark.django_db
def test_dish_str_method():
    ingredient = Ingredient.objects.create(name=TEST_INGREDIENT_NAME)
    assert str(ingredient) == TEST_INGREDIENT_NAME

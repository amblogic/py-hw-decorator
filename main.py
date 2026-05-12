import os
from logger_param import logger

path_cook = "cook_book.log"
path_shop_list = "shop_list.log"

if os.path.exists(path_cook):
    os.remove(path_cook)
if os.path.exists(path_shop_list):
    os.remove(path_shop_list)


@logger(path_cook)
def create_cook_book(filename):
    """Создает справочник для книги рецептов.

    Args:
        filename (str): абсолютный путь до файла.

    Return:
        cook_book: Словарь с ключами - названиями блюд и значениями - 
        ингридиентами.
    """

    with open(filename, encoding="utf-8") as file:
        cook_book = {}
        for line in file.read().split("\n\n"):
            name, _, *words = line.split("\n")
            recipe = []
            for word in words:
                ingredient_name, quantity, measure = map(
                    lambda x: int(x) if x.isdigit() else x, word.split(" | ")
                )
                recipe.append(
                    {
                        "ingredient_name": ingredient_name,
                        "quantity": quantity,
                        "measure": measure,
                    }
                )
            cook_book[name] = recipe
    return cook_book

@logger(path_shop_list)
def get_shop_list_by_dishes(dishes, person_count):
    """Создает список ингридиентов по списку рецептов для указанного 
        кол-ва персон.

    Args:
        dishes (list): список блюд.
        person_count (int): Кол-во персон.

    Return:
        total_ingridients: Словарь с ключами - названиями ингридиентов 
        и значениями - количеством необходимым для покупки на указанное 
        кол-во персон.
    """
    cook_book = create_cook_book(os.path.join(os.getcwd(), "recipes.txt"))
    total_ingridients = {}
    for dish in dishes:
        if dish in cook_book:
            for ingridient in cook_book.get(dish):
                ing_name = ingridient["ingredient_name"]
                if ing_name in total_ingridients:
                    total_ingridients[ing_name]["quantity"] += (
                        ingridient["quantity"] * person_count
                    )
                else:
                    total_ingridients[ing_name] = {
                        "measure": ingridient["measure"],
                        "quantity": ingridient["quantity"] * person_count,
                    }

    return total_ingridients


if __name__ == "__main__":
    print(get_shop_list_by_dishes(["Запеченный картофель", "Омлет"], 3))
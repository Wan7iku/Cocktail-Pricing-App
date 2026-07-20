from crud import get_all_ingredients

ingredients = get_all_ingredients()

print("Number of ingredients:", len(ingredients))

for ingredient in ingredients[:5]:
    print(
        ingredient.ingredient_id,
        ingredient.ingredient_name,
    )
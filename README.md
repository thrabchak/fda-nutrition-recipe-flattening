Definitions:
- Food: composed of ingredients in specific proportions
- Ingredient: Either a food or a base ingredient
- Base ingredient: An ingredient that is not composed of another ingredient

Problem:
- Some ingredients are foods themselves.
- We want a table showing the base ingredient proportions for each food.

Goal:
- Re-create table so that all foods are composed of base ingredients in the correct proportions.

Method:
1. Load csv
2. Identify all foods
3. Identify all base ingredients
4. Create a new table
	- Iterate through each food and create rows for each ingredient in the food
5. Write new table to csv

import os
import pandas as pd

def main():
	data_file = "fped_1718_trh.csv"

	data_folder = os.path.abspath("data")
	data_file_path = os.path.join(data_folder, data_file)

	printStep("Step 1: Loading CSV")
	df = load(data_file_path)

	printStep("Step 2: Find all foods")
	foods = findFoods(df)

	printStep("Step 3: Find all base ingredients")
	base_ingredients = findBaseIngredients(df, foods)

	printStep("Test: Pasta Alfredo Test")
	pasta_alfredo = 58146691
	recipe = simplifyRecipe(df, pasta_alfredo, base_ingredients)
	printRecipeSummary(recipe)

	# printStep("Step 4: Create a new table of foods")
	# new_table = createNewTable(df, foods, base_ingredients)

	printStep("Step 5: Write new table to CSV")
	save(recipe, data_file_path)

	printStep("Finished")

def printStep(str):
	print("\n" + str + "\n")

def printInfo(st):
	print("    - " + str(st))

def load(csv_file):
	printInfo("Loading: " + csv_file)
	df = pd.read_csv(csv_file)
	printInfo("Column names: " + str(df.columns))
	printInfo("Done")
	return df

def save(df, data_file_path):
	output_path = data_file_path[:-4] + "-output.csv"
	printInfo("Saving: " + output_path)
	df.to_csv(output_path, index=False)
	printInfo("Done")

def findFoods(df):
	foods = set()
	for index, row in df.iterrows():
		foods.add(row['foodcode'])
	printInfo("Number of foods found: " + str(len(foods)))
	return foods

def findBaseIngredients(df, foods):
	ingredients = set()
	for index, row in df.iterrows():
		ingredients.add(row['ingredientcode'])
	printInfo("Number of total ingredients found: " + str(len(ingredients)))

	complex_ingredients = set()
	for food in foods:
		if (food in ingredients):
			ingredients.remove(food)
			complex_ingredients.add(food)
	printInfo("Number of base ingredients found: " + str(len(ingredients)))
	printInfo("Number of complex_ingredients found: " + str(len(complex_ingredients)))

	return ingredients

def findRecipe(df, food):
	return df.loc[df['foodcode'] == food]

def simplifyRecipe(df, food, base_ingredients):
	printInfo("Finding recipe for: " + str(food))
	recipe = findRecipe(df, food)
	recipe_weight = recipe['recipeweight'].iloc[0]
	original_base_ingredients = []
	simplified_ingredients = []

	for index, row in recipe.iterrows():
		ingredient = row['ingredientcode']
		ingredient_weight = row['ingredientweightg']
		ingredient_percentage = (ingredient_weight/recipe_weight)

		if (ingredient in base_ingredients):
			new_row = row.copy()
			new_row['ingredientpercentage'] = ingredient_percentage
			original_base_ingredients.append(new_row)
		else:
			# This is a complex ingredient, so find the base ingredients
			complex_ingredient_recipe = simplifyRecipe(df, ingredient, base_ingredients)
			complex_ingredient_recipe['foodcode'] = food
			complex_ingredient_recipe['recipeweight'] = recipe_weight

			scaleRecipe(complex_ingredient_recipe, ingredient_weight, ingredient_percentage)

			simplified_ingredients.append(complex_ingredient_recipe)

	simplified_ingredients.append(pd.concat(original_base_ingredients, axis=1).T)
	output = pd.concat(simplified_ingredients)

	printRecipeSummary(output)
	return output

def scaleRecipe(recipe, new_weight, new_overall_scale):
	initial_recipe_weight = recipe['ingredientweightg'].sum()
	for index, row in recipe.iterrows():
		initial_ingredient_weigth = recipe['ingredientweightg']
		initial_ingredient_percentage = (initial_ingredient_weigth/initial_recipe_weight)
		recipe['ingredientweightg'] = (new_weight*initial_ingredient_percentage)
		recipe['ingredientpercentage'] = (new_overall_scale*initial_ingredient_percentage)

def createNewTable(df, foods, base_ingredients):
	recipes = []
	for food in foods:
		recipes.append(simplifyRecipe(food))
	new_table = pd.concat(recipes)

	printInfo("Number of recipes added: " + str(len(recipes)))
	return new_table

def printRecipeSummary(recipe):
	description = recipe['mainfooddescription'].iloc[0]
	printInfo("Summary: " + str(description) + '\n')
	print(str(recipe[['ingredientpercentage', 'ingredientweightg', 'ingredientdescription']]) + '\n')
	totals = recipe['ingredientweightg'].sum()
	print("Total weight: " + str(recipe['ingredientweightg'].sum()))
	print("total percentage: " + str(recipe['ingredientpercentage'].sum()))

if __name__ == "__main__":
	main()
import os
import sys
import pandas as pd

def evaluate_file(data_file):
	data_folder = os.path.abspath("data")
	data_file_path = os.path.join(data_folder, data_file)

	printStep("Step 1: Loading CSV")
	df = load(data_file_path)

	printStep("Step 2: Find all foods")
	foods = findFoods(df)

	printStep("Step 3: Find all base ingredients")
	base_ingredients = findBaseIngredients(df, foods)

	# printStep("Test: Pasta Alfredo Test")
	# pasta_alfredo = 58146691
	# new_table = simplifyRecipe(df, pasta_alfredo, base_ingredients)

	printStep("Step 4: Create a new table of foods")
	new_table = createNewTable(df, foods, base_ingredients)

	printStep("Step 5: Write new table to CSV")
	save(new_table, data_file_path)

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
	recipe = findRecipe(df, food)
	recipe_weight = recipe['ingredientweightg'].sum()
	description = str(recipe['mainfooddescription'].iloc[0])
	printInfo("Simplifying: " + str(food) + " - " + description + " - " + str(recipe_weight))
	original_base_ingredients = []
	simplified_ingredients = []

	for index, row in recipe.iterrows():
		ingredient = row['ingredientcode']
		ingredient_weight = row['ingredientweightg']
		ingredient_description = row['ingredientdescription']

		if (ingredient in base_ingredients or ingredient == food):
			new_row = row.copy()
			original_base_ingredients.append(new_row)
		else:
			# This is a complex ingredient, so find the base ingredients and scale to this recipe
			complex_ingredient_recipe = simplifyRecipe(df, ingredient, base_ingredients)

			printInfo("scaling: " + ingredient_description + " to " + str(ingredient_weight) + " recipe total: " + str(recipe_weight))
			complex_ingredient_recipe = scaleRecipe(complex_ingredient_recipe, ingredient_weight)
			printInfo("Scaled recipe:")
			printRecipeSummary(complex_ingredient_recipe)

			simplified_ingredients.append(complex_ingredient_recipe)

	if (len(original_base_ingredients) > 0):
		simplified_ingredients.append(pd.concat(original_base_ingredients, axis=1).T)
	output = pd.concat(simplified_ingredients)

	output['mainfooddescription'] = description
	output['foodcode'] = food
	output['recipeweight'] = recipe_weight
	output['ingredientpercentage'] = output['ingredientweightg']/recipe_weight

	printRecipeSummary(output)

	return output

def scaleRecipe(recipe, new_weight):
	scaled_recipe = recipe.copy()
	initial_recipe_weight = recipe['ingredientweightg'].sum()
	printInfo(initial_recipe_weight)

	for index, row in recipe.iterrows():
		initial_ingredient_weight = row['ingredientweightg']
		initial_ingredient_percentage = (initial_ingredient_weight/initial_recipe_weight)
		scaled_recipe.loc[index, 'ingredientweightg'] = (new_weight*initial_ingredient_percentage)

	scaled_recipe['recipeweight'] = scaled_recipe['ingredientweightg'].sum()
	return scaled_recipe

def createNewTable(df, foods, base_ingredients):
	recipes = []
	for food in foods:
		recipes.append(simplifyRecipe(df, food, base_ingredients))
	new_table = pd.concat(recipes)

	printInfo("Number of recipes added: " + str(len(recipes)))
	return new_table

def printRecipeSummary(recipe):
	description = recipe['mainfooddescription'].iloc[0]
	printInfo("Summary: " + str(description) + '\n')
	print(str(recipe[['ingredientpercentage', 'ingredientweightg', 'ingredientdescription', 'recipeweight']]) + '\n')
	totals = recipe['ingredientweightg'].sum()
	print("Total weight: " + str(recipe['ingredientweightg'].sum()))
	print("Total percentage: " + str(recipe['ingredientpercentage'].sum()))

if __name__ == "__main__":
	evaluate_file("fped_0506_trh.csv")
	evaluate_file("fped_0708_trh.csv")
	evaluate_file("fped_0910_trh.csv")
	evaluate_file("fped_1112_trh.csv")
	evaluate_file("fped_1314_trh.csv")
	evaluate_file("fped_1516_trh.csv")
	evaluate_file("fped_1718_trh.csv")
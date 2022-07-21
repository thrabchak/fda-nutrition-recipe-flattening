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

	printStep("Step 4: Create a new table of foods")
	new_table = createNewTable(df, foods, base_ingredients)

	printStep("Step 5: Write new table to CSV")
	save(new_table, data_file_path)

	printStep("Finished")

def printStep(str):
	print("\n" + str + "\n")

def printInfo(str):
	print("    - " + str)

def load(csv_file):
	printInfo("Loading: " + csv_file)
	df = pd.read_csv(csv_file)
	printInfo("Column names: " + str(df.columns))
	printInfo("Done")
	return df

def save(df, data_file_path):
	output_path = data_file_path[:-4] + "-output.csv"
	printInfo("Saving: " + output_path)
	df.to_csv(output_path)
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

	multi_level_ingredients = set()
	for food in foods:
		if (food in ingredients):
			ingredients.remove(food)
			multi_level_ingredients.add(food)
	printInfo("Number of base ingredients found: " + str(len(ingredients)))
	printInfo("Number of multi_level_ingredients found: " + str(len(multi_level_ingredients)))

	return ingredients


def createNewTable(df, foods, base_ingredients):
	printInfo("TODO")
	# Iterate through each food and create rows for each ingredient in the food
	return df

if __name__ == "__main__":
	main()
import os
import pandas as pd

def main():
	data_file = "fped_1718_trh.csv"

	data_folder = os.path.abspath("data")
	data_file_path = os.path.join(data_folder, data_file)

	# 1. Load csv
	printStep("Step 1: Loading CSV")
	df = load(data_file_path)

	# 2. Identify all base ingredients
	printStep("Step 2: Find all base ingredients")
	base_ingredients = findBaseIngredients(df)

	# 3. Identify all foods
	printStep("Step 3: Find all foods")
	foods = findFoods(df)

	# 4. Create a new table
	printStep("Step 4: Create a new table of foods")
	new_table = createNewTable(df, foods, base_ingredients)

	# 5. Write new table to csv
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
	printInfo("Done")
	return df

def save(df, data_file_path):
	output_path = data_file_path[:-4] + "-output.csv"
	printInfo("Saving: " + output_path)
	df.to_csv(output_path)
	printInfo("Done")

def findBaseIngredients(df):
	printInfo("TODO")
	return {}

def findFoods(df):
	printInfo("TODO")
	return {}

def createNewTable(df, foods, base_ingredients):
	printInfo("TODO")
	# Iterate through each food and create rows for each ingredient in the food
	return df

if __name__ == "__main__":
	main()
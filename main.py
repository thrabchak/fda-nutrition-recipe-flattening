import os
import pandas as pd

def main():
	data_folder = os.path.abspath("data")
	data_file = "fped_1718_trh.csv"

	# 1. Load csv
	printStep("Step 1: Loading CSV")
	load(os.path.join(data_folder, data_file))

	# 2. Identify all base ingredients
	printStep("Step 2: Find all base ingredients")

	# 3. Identify all foods
	printStep("Step 3: Find all foods")

	# 4. Create a new table
	printStep("Step 4: Create a new table of foods")
		# Iterate through each food and create rows for each ingredient in the food

	# 5. Write new table to csv
	printStep("Step 5: Write new table to CSV")

	print("Finished")

def printStep(str):
	print("\n" + str + "\n")

def printInfo(str):
	print("    - " + str)

def load(csv_file):
	printInfo("Loading: " + csv_file)
	df = pd.read_csv(csv_file)

if __name__ == "__main__":
	main()
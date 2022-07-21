import os
import pandas as pd

def main():
	data_folder = os.path.abspath("data")
	data_file = "fped_1718_trh.csv"
	load(os.path.join(data_folder, data_file))

	print("done")
	

def load(csv_file):
	print("Loading: " + csv_file)
	df = pd.read_csv(csv_file)

if __name__ == "__main__":
	main()
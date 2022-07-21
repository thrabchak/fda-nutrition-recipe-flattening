import pandas as pd

def main():
	data_file = "./data/fped_1718_trh.csv"
	load(data_file)

	print("done")
	

def load(csv_file):
	print("Loading: " + csv_file)
	df = pd.read_csv(csv_file)

if __name__ == "__main__":
	main()
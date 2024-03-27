import os
import csv
import itertools
import random

def getTitles(folder_path, output_file):
    with open(output_file, 'w', newline='') as output_csv:
        writer = csv.writer(output_csv)

        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"): 
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
                        reader = csv.reader(file)
                        next(reader)
                        first_column = [row[0] for row in reader]
                        data = first_column
                        transposed_data = list(map(list, itertools.zip_longest(*[iter(data)] * 1)))
                        writer.writerows(transposed_data)
                except Exception as e:
                    print(f"Error processing file '{filename}': {e}")

folder_path = "Libs"
output_file = "LibsTitles.csv"
getTitles(folder_path, output_file)

def getRandomTitles(csv_file, output_file, num_titles=100):
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        titles = [row[0] for row in reader]

    if len(titles) < num_titles:
        raise ValueError("Not enough titles in the CSV file.")

    selected_titles = random.sample(titles, num_titles)

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        for title in selected_titles:
            writer.writerow([title])

input_csv_file = "Titles/AllTitles.csv"
output_csv_file = "Shared.csv"

getRandomTitles(input_csv_file, output_csv_file)

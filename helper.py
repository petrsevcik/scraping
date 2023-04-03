import csv

def connect_csv_files(input_files: list, output_file: str):
    with open(output_file, "w") as outfile:
        writer = csv.writer(outfile)
        for i, file in enumerate(input_files):
            with open(file, "r") as infile:
                reader = csv.reader(infile)
                header = next(reader) # skip header
                if i == 0:
                    writer.writerow(header)
                writer.writerows(reader)

connect_csv_files(['pantarhei_books.csv', 'martinus_books.csv'], 'all_books.csv')

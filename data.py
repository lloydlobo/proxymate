import csv
import os
import sqlite3

if __name__ == "__main__":
    # Set up file paths
    dir_path = os.path.dirname(__file__)
    source_file_path = os.path.join(dir_path, "txt", "spock.txt")
    output_file_path = os.path.join(dir_path, "output.csv")

    # Read the input text from the source file
    input_text = read_source_file(source_file_path)

    # Clean up the input text and create the Markov model
    corpus = remove_serial_numbers(input_text.splitlines())
    text_model, state_size = generate_model(corpus)

    # Generate a sentence and print the output
    try:
        output_text = generate_sentence(text_model, 140)
        print(output_text)

        # Log the output to a CSV file
        with open(output_file_path, "a") as output_file:
            writer = csv.writer(output_file)
            writer.writerow([output_text])

    except ValueError as e:
        print(e)  # Sir, there is no reason to stand here and be insulted....

    # Store the output in a SQLite3 database
    conn = sqlite3.connect(os.path.join(dir_path, "output.db"))
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS output (id INTEGER PRIMARY KEY AUTOINCREMENT, output_text TEXT)"
    )

    cursor.execute("INSERT INTO output (output_text) VALUES (?)", (output_text,))
    conn.commit()
    conn.close()

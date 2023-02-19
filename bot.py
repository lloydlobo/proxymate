# Sir, there is no reason to stand here and be insulted....
import datetime
import os
import random
import re

import markovify


def read_source_file(file_path):
    """
    Reads the text file at the given file_path and returns the contents as a string.
    """
    try:
        with open(file_path) as f:
            input_text = f.read()
    except OSError as e:
        raise ValueError(f"Failed to read source text file: {e}")

    return input_text


def remove_serial_numbers(sentences):
    """
    Removes the serial number from each sentence in the list of sentences.
    """
    return [re.sub(r"^\d+[\.\)]\.?\s*", "", s).strip('"') for s in sentences]


# When the range is changed from (1,3) to (2,5), the possible values of state_size increase from 3 to 4. This means that text_model needs to consider more possible states when generating sentences. This can increase the computational complexity of generating the Markov model, which can in turn increase the time it takes to generate the model.
def generate_model(input_text):
    """
    Generates a Markov model for the input text.
    The state size is 1 if it's between 00:00:00 and 02:00:00, otherwise it's a random integer between 1 and 3.

    :param input_text: A string containing the input text.
    :return: A tuple containing the Markov model and the state size.
    """
    now = datetime.datetime.now().time()
    start_time = datetime.time(0, 0, 0)
    end_time = datetime.time(2, 0, 0)

    state_size = 1 if start_time <= now <= end_time else random.randint(1, 3)
    text_model = markovify.Text(input_text, state_size=state_size)

    return text_model, state_size


# This function uses the re module to extract all the words in the generated sentence and check whether there are any duplicates. If the sentence contains any duplicates, it discards it and generates a new one. If no valid sentence can be generated within 100 tries, the function returns None.
def generate_sentence(text_model, max_chars):
    """
    Generates a sentence using the given Markov model and limits it to max_chars characters,
    without any repeated words.

    :param text_model: A Markov model generated from the input text.
    :param max_chars: The maximum number of characters the generated sentence should have.
    :return: A string containing the generated sentence or None if no valid sentence can be generated.
    """
    if max_chars < 20:
        raise ValueError("max_chars should be at least 20")

    # Return an empty string if max_chars is exactly 20, to avoid errors in markovify
    if max_chars == 20:
        return ""

    sentence = None
    tries = 0
    while sentence is None and tries < 100:
        # Use make_sentence if max_chars is greater than 140
        if max_chars > 140:
            sentence = text_model.make_sentence(tries=100)
        else:
            # Use make_short_sentence if max_chars is less than or equal to 140
            sentence = text_model.make_short_sentence(max_chars=max_chars, tries=100)

        if sentence is not None:
            # Check if the sentence contains repeated words
            words = re.findall(r"\b\w+\b", sentence)
            if len(words) == len(set(words)):
                # Add an ellipsis to the end of the sentence and return it
                return sentence.strip().capitalize() + "..."

        tries += 1

    # return None # Commented out to try with old functions
    # return sentence
    if sentence is not None:
        # Check if the sentence contains repeated words
        words = re.findall(r"\b\w+\b", sentence)
        if len(words) == len(set(words)):
            # Add an ellipsis to the end of the sentence and return it
            print("Quality downgraded: ", sentence)
            return sentence.strip().capitalize() + "..."
        else:
            return generate_sentence_try_while(text_model, max_chars)


def generate_sentence_try_while(text_model, max_chars):
    """
    Generates a sentence using the given Markov model and limits it to max_chars characters.
    This function is used as a fallback when generate_sentence fails to generate a valid sentence.

    :param text_model: A Markov model generated from the input text.
    :param max_chars: The maximum number of characters the generated sentence should have.
    :return: A string containing the generated sentence or None if no valid sentence can be generated.
    """
    if max_chars < 20:
        raise ValueError("max_chars should be at least 20")
    # Return an empty string if max_chars is exactly 20, to avoid errors in markovify
    if max_chars == 20:
        return ""

    # Try to generate a sentence with the given max_chars value
    sentence = text_model.make_sentence(max_chars=max_chars)

    # If the sentence is None, try decreasing max_chars and calling make_sentence again
    while sentence is None and max_chars > 20:
        max_chars -= 10
        sentence = text_model.make_sentence(max_chars=max_chars)

    # If we still can't generate a sentence after several attempts, return None
    if sentence is None:
        return None

    # Check for repeating patterns
    words = sentence.split()
    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            return generate_sentence(text_model, max_chars)

    # Add an ellipsis to the end of the sentence and return it
    return sentence.strip() + "..."


if __name__ == "__main__":
    # Set up file paths
    dir_path = os.path.dirname(__file__)
    source_file_path = os.path.join(dir_path, "txt", "spock.txt")

    # Read the input text from the source file
    input_text = read_source_file(source_file_path)

    # Clean up the input text and create the Markov model
    corpus = remove_serial_numbers(input_text.splitlines())
    text_model, state_size = generate_model(corpus)

    # Generate a sentence and print the output
    try:
        output_text = generate_sentence(text_model, 140)
        print(output_text)
    except ValueError as e:
        print(e)  # Sir, there is no reason to stand here and be insulted....

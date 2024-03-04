# Preprocess YourText

Preprocess YourText is a Python package for text preprocessing tasks, designed to simplify and streamline the process of cleaning and preparing text data for natural language processing (NLP) tasks.

## Features

- **HTML Tag Removal**: Easily remove HTML tags from text data.
- **URL Removal**: Remove URLs from text data.
- **Email Removal**: Remove email addresses from text data.
- **Special Character Removal**: Remove special characters from text data.
- **Accent Removal**: Remove accents from characters in text data.
- **Contractions Expansion**: Expand contractions in text data (e.g., "don't" to "do not").
- **Lemmatization**: Lemmatize words in text data to their base form.
- **Spelling Correction**: Correct spelling mistakes in text data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Installation

You can install the package via pip:

```bash
pip install mngdataclean

## Usage
import mngdataclean as mdc

# Example usage:
text = "This is an example text with HTML tags <b>and URLs</b>."
clean_text = mdc.get_clean(text)
print(clean_text)

#output is 
This is an example text with HTML tags and URLs.




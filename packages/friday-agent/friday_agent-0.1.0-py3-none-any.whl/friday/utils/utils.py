import copy
import numpy as np
import itertools
import json
import logging
import os
import re
import string
from typing import Any
import tqdm
import re
import tiktoken
import random

def random_string(length):
    """
    Generates a random string of a specified length.

    This function creates a string consisting of random ASCII letters (both uppercase and lowercase) and digits.

    Args:
        length (int): The desired length of the random string.

    Returns:
        str: A string of random characters and digits of the specified length.
    """
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def num_tokens_from_string(string: str) -> int:
    """
    Calculates the number of tokens in a given text string according to a specific encoding.

    This function uses the encoding method for a specified model to determine the number of tokens
    that the text string would be broken into, which is especially useful for understanding how text
    will be tokenized in models like GPT-4.

    Args:
        text (str): The text string to be tokenized.

    Returns:
        int: The number of tokens the string is encoded into according to the model's tokenizer.
    """
    encoding = tiktoken.encoding_for_model('gpt-4-1106-preview')
    num_tokens = len(encoding.encode(string))
    return num_tokens



def parse_content(content, type="html.parser"):
    """
    Parses and cleans the given HTML content, removing specified tags, ids, and classes.

    This function uses BeautifulSoup to parse the HTML content based on the specified parser type. It excludes
    certain tags, ids, and classes that are generally not part of the main content, such as navigation bars,
    headers, and footers. After cleaning, it reports the reduction in content size.

    Args:
        content (str): The HTML content to be parsed and cleaned.
        type (str, optional): The type of parser to be used by BeautifulSoup. Defaults to "html.parser".
            Supported types include "html.parser", "lxml", "lxml-xml", "xml", and "html5lib".

    Raises:
        ValueError: If an unsupported parser type is specified.

    Returns:
        str: The cleaned text extracted from the HTML content.
    """
    implemented = ["html.parser", "lxml", "lxml-xml", "xml", "html5lib"]
    if type not in implemented:
        raise ValueError(f"Parser type {type} not implemented. Please choose one of {implemented}")

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(content, type)
    original_size = len(str(soup.get_text()))

    tags_to_exclude = [
        "nav",
        "aside",
        "form",
        "header",
        "noscript",
        "svg",
        "canvas",
        "footer",
        "script",
        "style",
    ]
    for tag in soup(tags_to_exclude):
        tag.decompose()

    ids_to_exclude = ["sidebar", "main-navigation", "menu-main-menu"]
    for id in ids_to_exclude:
        tags = soup.find_all(id=id)
        for tag in tags:
            tag.decompose()

    classes_to_exclude = [
        "elementor-location-header",
        "navbar-header",
        "nav",
        "header-sidebar-wrapper",
        "blog-sidebar-wrapper",
        "related-posts",
    ]
    for class_name in classes_to_exclude:
        tags = soup.find_all(class_=class_name)
        for tag in tags:
            tag.decompose()

    content = soup.get_text()
    content = clean_string(content)

    cleaned_size = len(content)
    if original_size != 0:
        logging.info(
            f"Cleaned page size: {cleaned_size} characters, down from {original_size} (shrunk: {original_size-cleaned_size} chars, {round((1-(cleaned_size/original_size)) * 100, 2)}%)"  # noqa:E501
        )

    return content


def clean_string(text):
    """
    Cleans a given string by performing various operations such as whitespace normalization,
    removal of backslashes, and replacement of hash characters with spaces. It also reduces
    consecutive non-alphanumeric characters to a single occurrence.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text after applying all the specified cleaning operations.
    """
    # Replacement of newline characters:
    text = text.replace("\n", " ")

    # Stripping and reducing multiple spaces to single:
    cleaned_text = re.sub(r"\s+", " ", text.strip())

    # Removing backslashes:
    cleaned_text = cleaned_text.replace("\\", "")

    # Replacing hash characters:
    cleaned_text = cleaned_text.replace("#", " ")

    # Eliminating consecutive non-alphanumeric characters:
    # This regex identifies consecutive non-alphanumeric characters (i.e., not
    # a word character [a-zA-Z0-9_] and not a whitespace) in the string
    # and replaces each group of such characters with a single occurrence of
    # that character.
    # For example, "!!! hello !!!" would become "! hello !".
    cleaned_text = re.sub(r"([^\w\s])\1*", r"\1", cleaned_text)

    return cleaned_text


def is_readable(s):
    """
    Heuristic to determine if a string is "readable" (mostly contains printable characters and forms meaningful words)

    :param s: string
    :return: True if the string is more than 95% printable.
    """
    try:
        printable_ratio = sum(c in string.printable for c in s) / len(s)
    except ZeroDivisionError:
        logging.warning("Empty string processed as unreadable")
        printable_ratio = 0
    return printable_ratio > 0.95  # 95% of characters are printable





def format_source(source: str, limit: int = 20) -> str:
    """
    Format a string to only take the first x and last x letters.
    This makes it easier to display a URL, keeping familiarity while ensuring a consistent length.
    If the string is too short, it is not sliced.
    """
    if len(source) > 2 * limit:
        return source[:limit] + "..." + source[-limit:]
    return source




# check if the source is valid json string
def is_valid_json_string(source: str):
    try:
        _ = json.loads(source)
        return True
    except json.JSONDecodeError:
        logging.error(
            "Insert valid string format of JSON. \
            Check the docs to see the supported formats - `https://docs.embedchain.ai/data-sources/json`"
        )
        return False




def chunks(iterable, batch_size=100, desc="Processing chunks"):
    """
    Breaks an iterable into smaller chunks of a specified size, yielding each chunk in sequence.

    This function is particularly useful for processing large iterables in manageable parts,
    optionally displaying a progress bar through tqdm for user feedback.

    Args:
        iterable (iterable): The iterable to be chunked.
        batch_size (int, optional): The size of each chunk. Defaults to 100.
        desc (str, optional): Description text to be displayed alongside the progress bar. Defaults to "Processing chunks".

    Yields:
        tuple: A chunk of the iterable, with a maximum length of `batch_size`.
    """
    it = iter(iterable)
    total_size = len(iterable)

    with tqdm(total=total_size, desc=desc, unit="batch") as pbar:
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            pbar.update(len(chunk))
            chunk = tuple(itertools.islice(it, batch_size))

def generate_prompt(template: str, replace_dict: dict):
    """
    Generates a string by replacing placeholders in a template with values from a dictionary.

    This function is useful for dynamically generating text based on a template where placeholders
    are replaced with specific values provided in a dictionary.

    Args:
        template (str): The template string containing placeholders to be replaced.
        replace_dict (dict): A dictionary where each key corresponds to a placeholder in the template
                             and each value is the replacement for that placeholder.

    Returns:
        str: The resulting string after all placeholders have been replaced with their corresponding values.
    """
    prompt = copy.deepcopy(template)
    for k, v in replace_dict.items():
        prompt = prompt.replace(k, str(v))
    return prompt

def cosine_similarity(a, b):
    """
    Calculates the cosine similarity between two vectors.

    This measure of similarity between two non-zero vectors of an inner product space that measures
    the cosine of the angle between them, with a range of [-1, 1].

    Args:
        a (array_like): The first vector.
        b (array_like): The second vector.

    Returns:
        float: The cosine similarity between vectors `a` and `b`.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\
    

    
# prompt =  '''
# 'Sheet1':                           Zone 1           Unnamed: 1 Unnamed: 2 Unnamed: 3  \
# 0                           Name                 Type    Revenue       Rent   
# 1              Rainforest Bistro           Restaurant      32771       1920   
# 2            Panorama Outfitters              Apparel      23170       1788   
# 3   Zack's Cameras and Trail Mix   Electronics / Food      33117       1001   
# 4          SignPro Custom DeSign              Signage      21246       1121   
# 5                         Zone 2                  NaN        NaN        NaN   
# 6      Serenity Indoor Fountains                Decor      25234       6359   
# 7                Budapest Comics               Comics      12251       2461   
# 8                Dottie's Lattes           Restaurant      34427       1293   
# 9                         Zone 3                  NaN        NaN        NaN   
# 10                Gumball Utopia                Candy      13271       3420   
# 11         Your Uncle's Basement  Sports Collectibles      11119       8201   
# 12    Carnivore Loan Specialists              Finance      31000      50312   
# 13            Harry's Steakhouse           Restaurant      46791       1327   
# 14       Two Guys Paper Supplies      Office Supplies      76201       1120   
# 15                  Dragon Pizza           Restaurant      10201       2000   
# 16                        Zone 4                  NaN        NaN        NaN   
# 17    Us Three: The U2 Fan Store                Music      10201       1200   
# 18               Jimmy's Buffett           Restaurant      10027       3201   
# 19       Franz Equipment Rentals  Industrial Supplies      20201       2201   
# 20           Nigel's Board Games          Board Games      62012       2013   
# 21              Destructor's Den        Baby Supplies      79915       5203   
# 22                    Hook Me Up       Sporting Goods      56503       1940   
# 23           Zone 5 (Food Court)                  NaN        NaN        NaN   
# 24                     Slam Dunk           Restaurant      61239       5820   
# 25  Ben's Hungarian-Asian Fusion           Restaurant      68303       2011   
# 26                 PleaseBurgers           Restaurant      20132       1402   
# 27                Reagan's Vegan           Restaurant      20201       6201   
# 28      FreshCart Store-to-Table           Restaurant      83533       2751   

#              Unnamed: 4  
# 0                Opened  
# 1   2023-07-19 00:00:00  
# 2   2023-06-11 00:00:00  
# 3   2023-05-12 00:00:00  
# 4   2023-01-30 00:00:00  
# 5                   NaN  
# 6   2023-05-01 00:00:00  
# 7   2023-01-03 00:00:00  
# 8   2023-05-31 00:00:00  
# 9                   NaN  
# 10  2023-11-04 00:00:00  
# 11  2023-01-10 00:00:00  
# 12  2023-03-09 00:00:00  
# 13  2023-01-08 00:00:00  
# 14  2023-09-20 00:00:00  
# 15  2023-01-20 00:00:00  
# 16                  NaN  
# 17  2023-09-20 00:00:00  
# 18  2023-01-20 00:00:00  
# 19  2023-03-06 00:00:00  
# 20  2023-01-07 00:00:00  
# 21  2023-02-06 00:00:00  
# 22  2023-05-07 00:00:00  
# 23                  NaN  
# 24  2023-10-20 00:00:00  
# 25  2023-02-12 00:00:00  
# 26  2023-02-15 00:00:00  
# 27  2023-07-20 00:00:00  
# 28  2023-12-08 00:00:00
#         '''
# print(num_tokens_from_string(prompt))


# {
#      "paths": {
#     "/tools/python": {
#       "post": {
#         "summary": "Execute Python",
#         "operationId": "execute_python_tools_python_post",
#         "requestBody": {
#           "content": {
#             "application/json": {
#               "schema": {
#                 "$ref": "#/components/schemas/Item"
#               }
#             }
#           },
#           "required": true
#         },
#         "responses": {
#           "200": {
#             "description": "Successful Response",
#             "content": {
#               "application/json": {
#                 "schema": {}
#               }
#             }
#           },
#           "422": {
#             "description": "Validation Error",
#             "content": {
#               "application/json": {
#                 "schema": {
#                   "$ref": "#/components/schemas/HTTPValidationError"
#                 }
#               }
#             }
#           }
#         }
#       }
#     }
#   }
# }
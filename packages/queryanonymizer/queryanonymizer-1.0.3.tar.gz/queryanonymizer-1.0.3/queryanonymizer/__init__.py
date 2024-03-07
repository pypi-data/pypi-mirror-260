__all__ = ['anonymize','deanonymize','keywords_list']

import string
import random
import re
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
import json
from enum import Enum
from typing import List
import os
from datetime import datetime, timedelta
import arrow
from unidecode import unidecode
import pandas as pd

class KeywordsGroup(Enum):
    CUSTOM_ONLY = 0
    SQL = 1
    TSQL = 2
    MySQL = 3
    PLSQL = 4
    DAX = 5

def keywords_list(keywords_group = KeywordsGroup.SQL,
                  custom_keywords: List[str] = [],
                  print_keywords: bool = True) -> list:
    """
    Generates a list of keywords based on a specified group and custom keywords.

    Args:
    keywords_group: An enumeration representing the group of keywords to be used.
    custom_keywords (List[str]): A list of custom keywords to be added.
    print_keywords (bool): If True, prints the list of keywords.

    Returns:
    list: A combined list of keywords from the specified group and custom keywords.

    Raises:
    FileNotFoundError: If the keywords JSON file is not found.
    json.JSONDecodeError: If the JSON file cannot be parsed.
    """
    if keywords_group.value == 0:
        query_keywords = []
    else:
        try:
            current_file_path = os.path.abspath(__file__)
            current_directory = os.path.dirname(current_file_path)
            json_file_path = os.path.join(current_directory, 'keywords.json')
        
            with open(json_file_path, 'r') as file:
                keywords = json.load(file)
                query_keywords = keywords[keywords_group.name]
        except FileNotFoundError:
            raise FileNotFoundError(f"Keywords JSON file not found at {json_file_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Error decoding JSON file at {json_file_path}")

    query_keywords = set(item.upper() for item in query_keywords)
    custom_keywords = set(item.upper() for item in custom_keywords)
    combined_keywords = list(query_keywords.union(custom_keywords))

    if print_keywords and combined_keywords:
        print(f"Keywords list has {len(combined_keywords)} elements:\n===========================")
        for keyword in sorted(combined_keywords):
            print(keyword)

    return combined_keywords


def anonymize(query: str = "",
              keywords_group=KeywordsGroup.SQL,
              custom_keywords: List[str] = [],
              custom_tokens: List[str] = [],
              prompt: str = "",
              print_result: bool = True,
              anonymize_string_literals: bool = True,
              anonymize_numbers: bool = True,
              anonymize_dates: bool = True,
              min_word_length: int = 3,
              path_to_query_file: str = "",
              path_to_custom_keywords_file: str = "",
              path_to_custom_tokens_file: str = "",
              path_to_prompt_file: str = "",
              path_to_anonymized_file: str = "",
              path_to_decoder_dictionary_file: str = "",
              format_date: str = 'YYYY-MM-DD',
              format_time: str = 'HH:mm:ss',
              format_datetime: str = 'YYYY-MM-DD HH:mm:ss'):

# Internal functions:
    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _assign_code_type(token_type):
        if token_type == 'datetime':
            return 'format'
        elif token_type == 'number':
            return 'number'
        else:
            return 'code'
        
    def _create_encryptor() -> str:
        letters = ''.join(random.sample(string.ascii_uppercase, 26))
        digits = ''.join(random.sample(string.digits, 10))
        return letters + digits
    
    def _identify_date_format_time(text: str, format_date: str = None, format_time: str = None, format_datetime: str = None):
        if not re.search(r'\d', text):
            return None

        for format_str in [format_datetime, format_date, format_time]:
            if format_str:
                try:
                    if '%' in format_str:
                        datetime.datetime.strptime(text, format_str)
                    else:
                        arrow.get(text, format_str)
                    return format_str
                except (ValueError, arrow.parser.ParserError):
                    continue

        return None

    def _anonymize_date(text, format_str: str = None):
        use_datetime = '%' in format_str
        try:
            if use_datetime:
                date_obj = datetime.strptime(text, format_str)
            else:
                date_obj = arrow.get(text, format_str).datetime
        except (ValueError, arrow.parser.ParserError):
            return text

        if "Y" in format_str and "H" in format_str:
            delta = timedelta(minutes=random.randint(1, 10000))
        elif "Y" in format_str:
            delta = timedelta(days=random.randint(1, 100))
        elif "H" in format_str:
            delta = timedelta(minutes=random.randint(1, 700))
        else:
            delta = timedelta(minutes=0)
        
        modified_date = date_obj + delta if random.choice([True, False]) else date_obj - delta

        if use_datetime:
            return modified_date.strftime(format_str)
        else:
            return arrow.get(modified_date).format(format_str)

    def _anonymize_number(text):
        try:
            number = int(text)

            if number > 99:
                current_year = datetime.now().year
                ranges = [
                    (1950, current_year - 6),
                    (current_year - 5, current_year),
                    (current_year + 1, current_year + 10),
                    (current_year + 11, current_year + 30)
                ]

                for start, end in ranges:
                    if start <= number <= end:
                        return str(random.randint(start, end))

                length = len(str(number))
                min_value = 10**(length - 1)
                max_value = 10**length - 1
                return str(random.randint(min_value, max_value))

            return text

        except ValueError:
            return text
    
    def _anonymize_word(to_anonymize: str, code: str) -> str:
        letters = string.ascii_uppercase
        letters_code = code[:26]
        numbers_code = code[26:]

        anonymized = ''
        to_anonymize = unidecode(to_anonymize)
        for char in to_anonymize:
            if char.isalpha():
                char_index = letters.index(char.upper())
                replacement_char = letters_code[char_index].lower() if char.islower() else letters_code[char_index]
                anonymized += replacement_char
            elif char.isdigit():
                anonymized += numbers_code[int(char)]
            else:
                anonymized += char

        return anonymized
        
    def _generate_code(row):
        if row['code_type'] == 'format':
            return _identify_date_format_time(row['unified'], format_date, format_time, format_datetime)
        elif row['code_type'] == 'code':
            return _create_encryptor()
        elif row['code_type'] == 'number':
            return 'number'
        else:
            return None
        
    def _generate_new_token(row):
        if row['code_type'] == 'format':
            return _anonymize_date(row['token'], row['code'])
        elif row['code_type'] == 'code':
            return _anonymize_word(row['token'], row['code'])
        elif row['token_type'] == 'number':
            return _anonymize_number(row['token'])
        else:
            return None
        
    def _extract_and_filter_words_with_apostrophes(source_text, pattern):
        words = re.findall(r"\b\w+\b|'\w+'", source_text)

        unique_words = list(set(words))

        filtered_words = [word for word in unique_words if re.search(pattern, word, re.IGNORECASE)]

        return filtered_words

# Main code:
    if path_to_query_file:
        with open(path_to_query_file, 'r') as file:
            if query:
                query += "\n"
            query += file.read()
    
    if path_to_prompt_file:
        with open(path_to_prompt_file, 'r') as file:
            if prompt:
                prompt += "\n"
            prompt += file.read()

    if path_to_custom_keywords_file:
        with open(path_to_custom_keywords_file, 'r') as file:
            if custom_keywords:
                custom_keywords.extend(json.load(file))
            custom_keywords = json.load(file)

    if path_to_custom_tokens_file:
        with open(path_to_custom_tokens_file, 'r') as file:
            if custom_tokens:
                custom_tokens.extend(json.load(file))
            custom_tokens = json.load(file)

    if query or path_to_query_file:
        query_keywords = keywords_list(keywords_group=keywords_group, custom_keywords=custom_keywords, print_keywords=False)
        query_keywords_upper = set([keyword.upper() for keyword in query_keywords])   
    else:
        query_keywords_upper = []
    
    # pattern = rf"(?:'([^']{{{min_word_length},}})')|(\b[a-zA-Z0-9_-]{{{min_word_length},}}\b)"
    pattern = r"(?:'([^']*)')|(\b[a-zA-Z0-9_-]*\b)"

    query_tokens = re.findall(pattern, query)
    prompt_tokens = re.findall(r'\[([^\]]*)\]', prompt)

    combined_tokens = query_tokens + [('', token) for token in prompt_tokens]
    
    if custom_tokens:
        modified_tokens = [token.replace('*', '.*') for token in custom_tokens]
        pattern = r"({})".format('|'.join(modified_tokens))

        filtered_words_with_apostrophes = _extract_and_filter_words_with_apostrophes(prompt, pattern)

        filtered_matches = []

        for word in filtered_words_with_apostrophes:
            if word.startswith("'") and word.endswith("'"):
                filtered_matches.append((word.strip("'"), ""))
            else:
                filtered_matches.append(("", word))

        combined_tokens.extend(filtered_matches)

    df_tokens = pd.DataFrame([{
        'token': token if token else non_apostrophe,
        'apostrophe_content': bool(token)
    } for token, non_apostrophe in combined_tokens], columns=['token', 'apostrophe_content'])
    df_tokens = df_tokens[df_tokens['token'] != '']
    df_tokens['unified'] = df_tokens['token'].str.upper()
    df_tokens['token_type'] = 'string word'

    for index, row in df_tokens.iterrows():
        token = row['token']
        if row['apostrophe_content']:
            if _identify_date_format_time(token, format_date, format_time, format_datetime) is None:
                df_tokens.at[index, 'token_type'] = 'string literal'
            else:
                df_tokens.at[index, 'token_type'] = 'datetime'
        elif token.upper() in query_keywords_upper:
            df_tokens.at[index, 'token_type'] = 'keyword'
        elif _is_float(token):
            df_tokens.at[index, 'token_type'] = 'number'

    df_tokens = df_tokens[df_tokens['token_type'] != 'keyword']

    upper_custom_tokens = [token.upper() for token in custom_tokens]
    df_tokens['not_removable'] = df_tokens['unified'].apply(lambda x: x.upper() in upper_custom_tokens)
    df_tokens = df_tokens[(df_tokens['token'].str.len() >= min_word_length) | (df_tokens['not_removable'] == True)]

    if not anonymize_dates:
        # df_tokens = df_tokens[df_tokens['token_type'] != 'datetime']
        df_tokens = df_tokens[(df_tokens['token_type'] != 'datetime') & (df_tokens['not_removable'] == False)]
    if not anonymize_string_literals:
        df_tokens = df_tokens[(df_tokens['token_type'] != 'string literal') & (df_tokens['not_removable'] == False)]
    if not anonymize_numbers:
        df_tokens = df_tokens[(df_tokens['token_type'] != 'number') & (df_tokens['not_removable'] == False)]

    df_tokens = df_tokens.drop_duplicates(subset=['token', 'token_type'])

    df_tokens['code_type'] = df_tokens['token_type'].apply(_assign_code_type)
    df_unified = df_tokens[['unified', 'code_type']].drop_duplicates().copy()

    df_unified['code'] = df_unified.apply(_generate_code, axis=1)

    df_tokens = df_tokens.merge(df_unified[['unified', 'code_type', 'code']], on=['unified', 'code_type'], how='left')

    del df_unified

    df_tokens['new_token'] = df_tokens.apply(_generate_new_token, axis=1)

    for index, row in df_tokens.iterrows():
        token = row['token']
        new_token = row['new_token']
        in_apostrophes = row['apostrophe_content']

        pattern = r"(?<='|\w)" + re.escape(token) + r"(?='|\w)" if in_apostrophes else r"(?<!'|\w)" + re.escape(token) + r"(?!'|\w)"
        query = re.sub(pattern, new_token, query)
        prompt = prompt.replace(f"[{token}]", new_token)
        prompt = re.sub(pattern, new_token, prompt)
    
    df_tokens['sort_order'] = df_tokens['unified'] + df_tokens['token_type'].str.upper()
    df_tokens.sort_values(by='sort_order', inplace=True)

    json_data = df_tokens.groupby(['token', 'new_token'])['token_type'].apply(list).to_dict()

    decoder_dictionary = {}
    for (token, new_token), token_types in json_data.items():
        if token not in decoder_dictionary:
            decoder_dictionary[token] = {}
        decoder_dictionary[token][new_token] = token_types

    if print_result:
        if prompt:
            print(prompt + "\n")
        if query:
            print(query + "\n")
        if len(decoder_dictionary) > 0:
            print(f"Decoder dictionary has {len(decoder_dictionary)} elements:\n===========================")
            for index, row in df_tokens.iterrows():
                print(f"{row['token']} ({row['token_type']}) -> {row['new_token']}")
    
    anonymized_query = query
    anonymized_prompt = prompt

    if path_to_decoder_dictionary_file:
        with open(path_to_decoder_dictionary_file, 'w') as file:
            json.dump(decoder_dictionary, file, sort_keys=True, indent=4)
    
    if path_to_anonymized_file:
        with open(path_to_anonymized_file, 'w') as file:
            file.write(f"{anonymized_prompt}\n{anonymized_query}")

    return anonymized_query, decoder_dictionary, anonymized_prompt


def deanonymize(anonymized_text: str = "",
                decoder_dictionary: str = "",
                path_to_decoder_dictionary_file: str = "",
                path_to_anonymized_file: str = "",
                path_to_deanonymized_file: str = "",
                print_result: bool = True) -> str:
    """
    Decrypts anonymized text based on a decoding dictionary.

    This function can take either text and a dictionary directly, or paths to files containing the anonymized text and the dictionary. If a path is provided for the output, it will write the deanonymized text to that file.

    Args:
    anonymized_text (str): Text to be decrypted. If not provided, the function reads from the specified file.
    path_to_decoder_dictionary_file (str): Path to the JSON file with the decoding dictionary.
    path_to_anonymized_file (str): Path to the file with anonymized text.
    path_to_deanonymized_file (str): Path to the file where the deanonymized text will be written.
    print_result (bool): Whether to print the deanonymized text to the console. Default is True.

    Returns:
    str: The deanonymized text.

    Raises:
    FileNotFoundError: If any specified file does not exist.
    json.JSONDecodeError: If the JSON file is malformed.
    IOError: If there is an error writing to the output file.
    """
    if path_to_decoder_dictionary_file:
        try:
            with open(path_to_decoder_dictionary_file, 'r') as file:
                decoder_dictionary_file = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Decoder dictionary file not found: {path_to_decoder_dictionary_file}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Error decoding JSON file", path_to_decoder_dictionary_file, 0)
    else:
        decoder_dictionary_file = {}
    
    if decoder_dictionary == "":
        decoder_dictionary = {}
    
    decoder_dictionary_json = {**decoder_dictionary_file, **decoder_dictionary}

    if path_to_anonymized_file:
        try:
            with open(path_to_anonymized_file, 'r') as file:
                anonymized_text = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Anonymized text file not found: {path_to_anonymized_file}")

    for token, anonymized_tokens in decoder_dictionary_json.items():
        for anonymized_token, types in anonymized_tokens.items():
            for token_type in types:
                if token_type in ["string literal", "datetime"]:
                    pattern = f"'{anonymized_token}'"
                    token = f"'{token}'"
                else:
                    pattern = r'\b' + re.escape(anonymized_token) + r'\b'

                anonymized_text = re.sub(pattern, token, anonymized_text)
    
    deanonymized_text = anonymized_text

    if print_result:
        print(deanonymized_text)

    if path_to_deanonymized_file:
        try:
            with open(path_to_deanonymized_file, 'w') as file:
                file.write(deanonymized_text)
        except IOError:
            raise IOError(f"Error writing to deanonymized text file: {path_to_deanonymized_file}")

    return deanonymized_text

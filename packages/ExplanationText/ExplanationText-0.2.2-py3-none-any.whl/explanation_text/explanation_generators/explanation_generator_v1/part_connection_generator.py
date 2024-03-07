import random

from explanation_text.explanation_generators.explanation_generator_v1.information_generator import generate_part_information


def generate_random_part_connection(single_object):
    text = ""
    if 'parts' in single_object:
        try:
            for part in single_object['parts']:
                connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
                text += (f"{part['part_label']} is {connection} connected to "
                         + single_object['label'] + ". ")
        except KeyError:
            print(single_object)
    return text


def generate_random_part_connection_with_information(single_object, api_token):
    text = ""
    if 'parts' in single_object:
        for part in single_object['parts']:
            connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
            text += f"{part['part_label']} is {connection} connected to " + single_object['label'] + ". "
            text += generate_part_information(single_object, part['part_label'], 30, api_token) + ". "
    return text

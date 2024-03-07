"""
File with general utility functions for the explanation generator
"""
from collections import defaultdict


def validate_and_parse_image(image, mode, minimum_relevance, minimum_part_count, maximum_part_count):
    """
    Function to parse, validate and sort content of labels dictionary
    """
    if 'objects' not in image or image.get('objects') == "":
        return [], []

    object_list = []
    new_objects = []
    objects = image.get('objects')
    all_probabilities_given = True

    for single_object in objects:

        if 'label' not in single_object or single_object.get('label') == "":
            break

        object_list.append(single_object.get('label'))
        if 'probability' in single_object:
            single_object.update({'probability': float_to_percentage(single_object.get('probability'))})
        else:
            all_probabilities_given = False

        if 'parts' not in single_object:
            break

        if 'heatmap' in single_object:
            del single_object['heatmap']

        if 'parts' not in single_object or len(single_object.get('parts')) < 1:
            single_object.pop('parts')
        else:
            # parse part labels
            parts = single_object.get('parts')
            sorted_parts = []
            for part in parts:
                if 'labels' in part and single_object.get('label') in part.get('labels') \
                        and len(part.get('labels').get(single_object.get('label'))) > 0:
                    new_part = {
                        "part_label": create_sentence_from_list(part.get('labels').get(single_object.get('label')))}
                    if 'img' in part:
                        new_part.update({'img': part.get('img')})
                    if 'relevancy' in part:
                        try:
                            # Check if relevance is greater than minimum relevance
                            relevance = float_to_percentage(part.get('relevancy'))
                            if relevance >= minimum_relevance or len(sorted_parts) < minimum_part_count:
                                new_part.update({'relevance': relevance})
                                sorted_parts.append(new_part)
                        except ValueError:
                            print(str(part.get('relevance')
                                      + " is not a valid value for relevance in object "
                                      + single_object.get('label')))
                    else:
                        sorted_parts.append(new_part)
                elif 'label' in part:
                    new_part = {"part_label": part.get('label')}
                    if 'img' in part:
                        new_part.update({'img': part.get('img')})
                    if 'relevancy' in part:
                        try:
                            # Check if relevance is greater than minimum relevance
                            relevance = float_to_percentage(part.get('relevancy'))
                            if relevance >= minimum_relevance or len(sorted_parts) < minimum_part_count:
                                new_part.update({'relevance': relevance})
                                sorted_parts.append(new_part)
                        except ValueError:
                            print(str(part.get('relevance')
                                      + " is not a valid value for relevance in object "
                                      + single_object.get('label')))
                    else:
                        sorted_parts.append(new_part)
                else:
                    pass
                    # print(part.get('labels'))

            # Group parts with same part_label if mode is GeoGuesser
            if mode == str.lower('ExplanationGeneratorGG'):
                sorted_parts = group_parts(sorted_parts)

            # Sort part labels
            sorted_parts = sorted(sorted_parts, key=lambda d: d['relevance'], reverse=True)
            if len(sorted_parts) > 0:
                single_object.update({'parts': sorted_parts[:maximum_part_count]})
            else:
                single_object.pop('parts')

        new_objects.append(single_object)

    if all_probabilities_given:
        # Sort objects
        sorted_objects = sorted(new_objects, key=lambda d: d['probability'], reverse=True)
        return object_list, sorted_objects

    return object_list, new_objects


def group_parts(part_list):
    """
    Function to group parts with same part_label
    :param part_list: list of parts
    This function groups parts with the same part_label into a single dictionary.
    The dictionary keeps track of the label and the original images and relevance of the parts.
    In addition, the count of parts and the sum of relevance (here just 'relevance') is also stored.

    """
    # Dictionary to store grouped parts
    grouped_parts = defaultdict(lambda: {'part_label': '', 'relevance': 0, 'images': [], 'count': 0,
                                         'individual_relevance': []})

    group_found = False

    # Group parts by part_label
    for part in part_list:
        label = part['part_label']
        grouped_parts[label]['part_label'] = label
        grouped_parts[label]['count'] += 1
        grouped_parts[label]['individual_relevance'].append(part['relevance'])
        grouped_parts[label]['relevance'] += part['relevance']
        grouped_parts[label]['images'].append(part['img'])

        if grouped_parts[label]['count'] > 1:
            group_found = True

    # If no group is found, return part_list as is
    if not group_found:
        return part_list

    # Iterate over grouped_parts and update part_list for parts with multiple occurrences
    for label, info in grouped_parts.items():
        if info['count'] > 1:
            # Remove all original parts and add the single grouped part
            part_list = [part for part in part_list if part['part_label'] != label]
            part_list.append(grouped_parts[label])

    return part_list


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        if 0 < a < 1:
            return round(float(a) * 100)

        return 100
    except ValueError:
        return 0


def create_sentence_from_list(word_list):
    """
    Method to parse a list of labels to a string
    of the format <label1>, <label2>, ... and <labelN>
    """
    if not word_list:
        return ""

    if len(word_list) == 1:
        return word_list[0]

    sentence = ", ".join(word_list[:-1]) + " and " + word_list[-1]
    return sentence


def dict_to_lowercase(input_data):
    """
    Function to lowercase input data, except for the value of a key "img"
    """
    if isinstance(input_data, dict):
        # If the input is a dictionary, recursively convert keys and values to lowercase
        return {key.lower(): dict_to_lowercase(value) if key.lower() != "img" else value for key, value in input_data.items()}
    elif isinstance(input_data, list):
        # If the input is a list, recursively convert elements to lowercase
        return [dict_to_lowercase(item) for item in input_data]
    elif isinstance(input_data, tuple):
        # If the input is a tuple, recursively convert elements to lowercase
        return tuple(dict_to_lowercase(item) for item in input_data)
    elif isinstance(input_data, str):
        # If the input is a string, convert it to lowercase
        return input_data.lower()
    else:
        # For other types, return as is
        return input_data


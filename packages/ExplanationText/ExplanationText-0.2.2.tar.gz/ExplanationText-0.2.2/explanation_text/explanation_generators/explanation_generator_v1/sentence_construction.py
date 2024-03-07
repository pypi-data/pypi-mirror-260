def generate_explanation_with_sentence_construction(single_object):
    """
    Main method for explanation with sentence construction
    Current version:
        'Object in image was classified as a <main label> with <percentage>% certainty.
        The <main label> was mainly classified that way, because of the <part label>
        with <percentage>% relevance at position <position> , <more part labels> ... and <last part label>'
    """
    explanation = ""
    if len(single_object) < 1:
        return explanation

    # main label sentence
    explanation += generate_main_label_explanation(single_object)

    # part labels sentence
    if 'parts' not in single_object:
        return explanation[:-1]
    explanation += generate_part_label_explanation(single_object)

    return explanation


def generate_main_label_explanation(single_object):
    """
    Method to construct main label sentence
    """

    main_label = single_object.get('label')
    explanation = f"The object in image was classified as a {main_label}"

    # main label percentage
    if 'probability' in single_object:
        main_label_percentage = single_object.get('probability')
        explanation += " with " + str(main_label_percentage) + "% certainty. "
    else:
        return explanation + "."

    return explanation


def generate_part_label_explanation(single_object):
    """
    Method to construct part label sentence
    """

    # get main label
    if 'label' in single_object:
        main_label = single_object.get('label')
    else:
        main_label = "object"

    # Start of the second sentence
    explanation = "The " + str(main_label) + " was mainly classified that way, because of the "

    # sentence part for each part label
    for part in single_object.get('parts'):

        # should key be 'part_label' or 'partLabel'?
        part_label = part.get('part_label')

        # add part label
        explanation += str(part_label)

        # optionally add relevance and position if given in sample
        if 'relevance' in part:
            relevance = part.get('relevance')
            explanation += " with " + str(relevance) + "% relevance"

        explanation += ", "

    # fix format of last part explanation and return explanation
    return format_explanation(explanation, single_object)


def format_explanation(explanation, single_object):
    """
    Method fix format issues with last part explanation sentence.
    Add dot at the end and replace last comma with 'and'.
    """
    if explanation.endswith(" "):
        explanation = explanation[:-2] + "."

    if 'parts' in single_object:
        last_comma_index = explanation.rfind(",")
        explanation = explanation[:last_comma_index] + " and" + explanation[last_comma_index + 1:]

    return explanation


def float_to_percentage(a):
    """
    Method parse float string to percentage string
    """
    try:
        return str(round(float(a) * 100))
    except ValueError:
        return "0.0"

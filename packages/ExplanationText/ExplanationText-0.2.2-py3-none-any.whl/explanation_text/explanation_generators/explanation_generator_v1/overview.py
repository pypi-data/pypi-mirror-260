def generate_explanation_with_overview(image, object_list):
    """
    Main method for explanation with overview
    Current version:
        'This image contains a <main_label>, a <main_label>, ... and a <main_label>'
    """

    if len(object_list) < 1:
        # optional addition: This might be due to the image containing no objects that are known to the AI.
        return "There were no objects detected in this image."

    explanation = "This image contains"

    # Case for one object
    if len(object_list) == 1:
        explanation += " a " + object_list[0] + "."

    # Case for multiple objects
    else:
        last_object = object_list[-1]
        for object_label in object_list[0:-1]:
            explanation += " a " + object_label + ","

        # add last object and dot
        explanation = explanation[:-1] + " and a " + last_object + "."

    return explanation

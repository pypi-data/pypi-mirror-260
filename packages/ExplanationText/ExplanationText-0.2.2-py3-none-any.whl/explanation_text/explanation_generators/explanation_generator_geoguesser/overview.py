import random
import string

# sentence templates

overview_sentences = ["The image was classified as {0}.",
                      "The image was identified as {0}.",
                      "The image's location was classified as {0}.",
                      "The image's location was determined to be {0}.",
                      "The image's location has been determined to be {0}.",
                      "The image's geographical origin has been classified as {0}.",
                      "The location of the image was classified as {0}.",
                      "The location of the image was determined to be {0}.",
                      "The identified location for this image is {0}.",
                      "The model identified the image as {0}.",
                      "The model classified the image as {0}.",
                      "The model classified the location of the image as {0}.",
                      "The model determined that the image was captured in {0}.",
                      "The model determined that the image was most likely captured in {0}.",
                      "Our model classified the image as {0}.",
                      "Our system classified the image as {0}.",
                      "Our system determined that the image was most likely captured in {0}."]


def generate_overview_text(location):
    """
    Method to generate overview text for GeoGuesser
    """

    if len(location) != 1:
        return "There was a problem with the classification of the image."

    location_name = string.capwords(location[0])

    return random.choice(overview_sentences).format(location_name)

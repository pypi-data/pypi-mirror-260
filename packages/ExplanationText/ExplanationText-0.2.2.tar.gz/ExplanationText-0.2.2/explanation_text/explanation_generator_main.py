import copy
import time

from explanation_text.explanation_generator_utils import validate_and_parse_image, dict_to_lowercase
from explanation_text.explanation_generators.api_test.api_test import generate_explanation_with_api_test
from explanation_text.explanation_generators.explanation_generator_geoguesser.main import generate_gg_overview, \
    generate_gg_medium, generate_gg_detailed
from explanation_text.explanation_generators.explanation_generator_v1.main import generate_egv1_overview, \
    generate_egv1_medium, generate_egv1_detailed
from explanation_text.explanation_generators.explanation_generator_v1.overview import generate_explanation_with_overview
from explanation_text.explanation_generators.explanation_generator_v1.sentence_construction import \
    generate_explanation_with_sentence_construction


class ExplanationGenerator:
    """
    Main class of Explanation Generator that runs generation methods of
    different text generation methods with given mode.
    """

    def __init__(self, api_token="", google_api_token="", mode="ExplanationGeneratorGG",
                 minimum_relevance=0):
        """
        Constructor sets explanation mode, default one is sentence construction.
        """
        self.api_token = api_token
        self.google_api_token = google_api_token
        self.mode = str.lower(mode)
        self.minimum_relevance = minimum_relevance

    def generate_explanation(self, image, minimum_part_count=2, maximum_part_count=5, return_time=False):
        """
        Main method to generate text explanation for given image.
        Returns Explanation text for mode overview and individual ones for each object
        """
        image_copy = copy.deepcopy(image)
        image_lower = dict_to_lowercase(image_copy)
        # Validate input
        label_list, object_list = validate_and_parse_image(image_lower, self.mode, self.minimum_relevance,
                                                           minimum_part_count, maximum_part_count)
        full_explanation = {}

        # Overview Mode
        overview_text = ""
        if self.mode == str.lower('OverviewBasic'):
            overview_text = generate_explanation_with_overview(object_list, label_list)
        elif self.mode == str.lower('ExplanationGeneratorV1'):
            overview_text = generate_egv1_overview(object_list, label_list, self.api_token)
        elif self.mode == str.lower('ExplanationGeneratorGG'):
            overview_text = generate_gg_overview(label_list)
        else:
            print("The desired text explanation overview mode " + self.mode
                  + " isn't implemented yet")
        full_explanation.update({"overview": overview_text})

        measured_times = []
        for single_object in object_list:
            start_time = time.time()
            object_name = single_object.get("label")

            # Medium Mode
            medium_text = ""
            if self.mode == str.lower('SentenceConstruction'):
                medium_text = generate_explanation_with_sentence_construction(single_object)
            elif self.mode == str.lower('ApiTest'):
                medium_text = generate_explanation_with_api_test(single_object)
            elif self.mode == str.lower('ExplanationGeneratorV1'):
                medium_text = generate_egv1_medium(single_object, self.api_token)
            elif self.mode == str.lower('ExplanationGeneratorGG'):
                medium_text = generate_gg_medium(single_object, self.api_token, False)
            else:
                print("The desired text explanation mode " + self.mode + " isn't implemented yet")

            # Detailed Mode
            detailed_text = ""
            if self.mode == str.lower('SentenceConstruction'):
                detailed_text = generate_explanation_with_sentence_construction(single_object)
            elif self.mode == str.lower('ApiTest'):
                detailed_text = generate_explanation_with_api_test(single_object)
            elif self.mode == str.lower('ExplanationGeneratorV1'):
                detailed_text = generate_egv1_detailed(single_object, self.api_token)
            elif self.mode == str.lower('ExplanationGeneratorGG'):
                detailed_text = generate_gg_detailed(single_object, self.api_token, self.google_api_token, False)

            # Append to return value
            while object_name in full_explanation:
                object_name = object_name + "_"
            full_explanation.update({object_name: {"medium": medium_text, "detailed": detailed_text}})

            # measureTime
            end_time = time.time()
            measured_times.append(end_time - start_time)

        if return_time:
            average_time = round(sum(measured_times) / max(len(measured_times), 1), 2)
            print("Average time for generating explanation per object: "
                  + str(average_time) + " sec")
            return full_explanation, average_time

        return full_explanation

    def generate_overview_gg(self, image, minimum_part_count=2, maximum_part_count=5):
        """
        Method to return overview explanation text with GeoGuesser
        """
        # Validate and parse input
        image_copy = copy.deepcopy(image)
        image_lower = dict_to_lowercase(image_copy)
        label_list, object_list = validate_and_parse_image(image_lower, self.mode, self.minimum_relevance,
                                                           minimum_part_count, maximum_part_count)

        # Call overview generation function
        overview_text = generate_gg_overview(label_list)
        return {"overview": overview_text}

    def generate_medium_gg(self, image, fallback=False, minimum_part_count=2, maximum_part_count=5):
        """
        Method to return medium explanation text with GeoGuesser
        If fallback is set, the generation falls back to version without language model
        """
        # Validate and parse input
        image_copy = copy.deepcopy(image)
        image_lower = dict_to_lowercase(image_copy)
        label_list, object_list = validate_and_parse_image(image_lower, self.mode, self.minimum_relevance,
                                                           minimum_part_count, maximum_part_count)

        # test if only one object is given
        if len(object_list) != 1:
            return {"medium": ""}

        # Call main explanation generation function for detailed
        medium_text = generate_gg_medium(object_list[0], self.api_token, fallback)
        return {"medium": medium_text}

    def generate_detailed_gg(self, image, fallback=False, minimum_part_count=2, maximum_part_count=5):
        """
        Method to return detailed explanation text with GeoGuesser
        If fallback is set, the generation falls back to version without language model
        """

        # Validate and parse input
        image_copy = copy.deepcopy(image)
        image_lower = dict_to_lowercase(image_copy)
        label_list, object_list = validate_and_parse_image(image_lower, self.mode, self.minimum_relevance,
                                                           minimum_part_count, maximum_part_count)

        # test if only one object is given
        if len(object_list) != 1:
            return {"detailed": ""}

        # Call main explanation generation function for detailed
        detailed_text = generate_gg_detailed(object_list[0], self.api_token, self.google_api_token, fallback)
        return {"detailed": detailed_text}


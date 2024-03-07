from explanation_text.explanation_generators.explanation_generator_v1.information_generator \
    import generate_object_information
from explanation_text.explanation_generators.explanation_generator_v1.part_connection_generator \
    import generate_random_part_connection, generate_random_part_connection_with_information
from explanation_text.explanation_generators.rephraser import rephrase
from explanation_text.explanation_generators.explanation_generator_v1.overview import generate_explanation_with_overview
from explanation_text.explanation_generators.explanation_generator_v1.sentence_construction import \
    generate_explanation_with_sentence_construction

PRINT_COMPONENT_TEXTS = False


def generate_egv1_overview(image, object_list, api_token):
    basic_overview_text = generate_explanation_with_overview(image, object_list)
    if PRINT_COMPONENT_TEXTS:
        print("  Overview text: " + basic_overview_text)
    return rephrase("strict", basic_overview_text, api_token)


def generate_egv1_medium(single_object, api_token):
    sentence_construction_text = generate_explanation_with_sentence_construction(single_object)
    part_connection = generate_random_part_connection(single_object)
    combined_text = sentence_construction_text + " " + part_connection
    if PRINT_COMPONENT_TEXTS:
        print("  Medium PartConnection text: " + part_connection)
    rephrase_text = rephrase("strict", combined_text, api_token)
    return rephrase_text


def generate_egv1_detailed(single_object, api_token):
    sentence_construction_text = generate_explanation_with_sentence_construction(single_object)
    object_information = generate_object_information(single_object, 30, api_token)
    part_connection = generate_random_part_connection_with_information(single_object, api_token)
    combined_text = object_information + " " + sentence_construction_text + " " + part_connection
    if PRINT_COMPONENT_TEXTS:
        print("  Detailed ObjectInformation text: " + object_information)
        print("  Detailed PartConnection text: " + part_connection)
    rephrase_text = rephrase("variable", combined_text, api_token)
    return rephrase_text

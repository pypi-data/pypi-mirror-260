from transformers import AutoTokenizer

from explanation_text.explanation_generators.api_utils import query_text_generation
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.knowledge_base_controller \
    import get_prefiltered_information
from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.landmark_detection import \
    detect_landmark

endpoint = "https://api-inference.huggingface.co/models/"

landmark_classes = ["building", "house"]
# old classes
# "monastery", "palace", "residence", "religious residence", "apiary", "boathouse", "place of worship", "church",
# "mosque", "theater", "cinema", "library", "planetarium", "restaurant", "prison", "institution"


def generate_part_information(use_landmark_detection, location, part, api_token, google_vision_api_key):
    information = ""
    part_label = str(part.get("part_label")).replace('_', ' ')

    # Check if landmark detection is available and detects landmark
    if use_landmark_detection and part_label.lower() in landmark_classes:
        # Check if part has multiple images. If there's only a single image, put it in a list
        images = part["images"] if "images" in part else [part["img"]]
        for image in images:
            landmark_detection_information = detect_landmark(part_label, image, google_vision_api_key)
            if landmark_detection_information != "":
                information += landmark_detection_information + " "
                return information

    # else: generate information from knowledge base
    information += filter_part_information_from_text(location, part_label.replace(' ', '_'), api_token)
    return information


def filter_part_information_from_text(location, part_label, api_token):
    prefiltered_information = get_prefiltered_information(location, part_label, 0.5, 300)
    if len(prefiltered_information) == 0:
        print("  ! Could not find information about " + part_label)
        return ""
    filtered_information = combine_knowledgebase_information(part_label.replace('_', ' '), prefiltered_information, api_token)
    return remove_words_after_last_dot(filtered_information)


def combine_knowledgebase_information(part_label, part_information, api_token):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    prompt = ("<s>[INST] Knowledge base: " + part_information
              + ". Merge by context and output information about " + part_label +
              " from your knowledge base.\n[/INST]")
    model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    max_new_tokens = int(tokenizer(part_information, return_length=True).length[0])

    configuration = {'return_full_text': False,
                     'max_new_tokens': max_new_tokens,
                     'num_return_sequences': 1,
                     'no_repeat_ngram_size': 3,
                     'max_time': 120.0,
                     'num_beams': 3,
                     'do_sample': True,
                     'top_p': 0.92,
                     'temperature': 0.6}

    query = ["", "", model_id, prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return return_text
    else:
        print("! Failed to obtain part information about " + part_label)
        return ""


def remove_words_after_last_dot(text):
    last_dot_index = text.rfind('.')
    return text[:last_dot_index + 1] if last_dot_index != -1 else text

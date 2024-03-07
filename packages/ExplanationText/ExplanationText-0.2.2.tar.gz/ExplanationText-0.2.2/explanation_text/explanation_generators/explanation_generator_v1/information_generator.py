from explanation_text.explanation_generators.api_utils import query_text_generation

ENDPOINT = "https://api-inference.huggingface.co/models/"


def generate_object_information(single_object, length, api_token):
    input_object = single_object.get("label")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

    configuration = {'return_full_text': False, 'num_return_sequences': 1, 'max_new_tokens': length,
                     'no_repeat_ngram_size': 1, 'max_time': 120.0, 'num_beams': 1,
                     'do_sample': True, 'top_k': length, 'top_p': 0.9,
                     'temperature': 0.5}
    prompt = "<|prompter|>Explain the main function of the following object: " + input_object + \
             " Explanation:<|endoftext|><|assistant|>"
    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]

    (success, return_text) = query_text_generation(query, ENDPOINT, headers)
    if success:
        return text_bis_letzter_punkt(return_text)
    return ""


def generate_part_information(single_object, part, length, api_token):
    input_object = single_object.get("label")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

    configuration = {'return_full_text': False, 'num_return_sequences': 1, 'max_new_tokens': length,
                     'no_repeat_ngram_size': 1, 'max_time': 120.0, 'num_beams': 1,
                     'do_sample': True, 'top_k': length, 'top_p': 0.9,
                     'temperature': 0.9}
    prompt = ("<|prompter|>Explain the main function of an " + part + " in object: "
              + input_object + " Explanation:<|endoftext|><|assistant|>")
    query = ["", "", "OpenAssistant/oasst-sft-1-pythia-12b", prompt, configuration]

    (success, return_text) = query_text_generation(query, ENDPOINT, headers)
    if success:
        return text_bis_letzter_punkt(return_text)
    return ""


def text_bis_letzter_punkt(text):
    index = text.rfind('.')
    if index != -1:
        return text[:index + 1]

    return ''

import re
from transformers import AutoTokenizer

from explanation_text.explanation_generators.api_utils import query_text_generation
from explanation_text.explanation_generators.explanation_generator_geoguesser.information_generator import remove_words_after_last_dot


def rephrase(mode, input_text, api_token, prompt=None):
    endpoint = "https://api-inference.huggingface.co/models/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    # mostly arbitrary length as it should not be reached anyway
    max_length = 4096 * 2
    tokenized_input = tokenizer(input_text, truncation=True, max_length=max_length, return_length=True)
    num_input_tokens = tokenized_input.length[0]

    num_output_tokens = int(1.2 * num_input_tokens)
    # use truncated input if original is too long
    if num_input_tokens >= max_length:
        input_text = remove_words_after_last_dot(tokenizer.decode(tokenized_input.input_ids, skip_special_tokens=True))

    # replace multiple whitespaces with a single whitespace
    input_text = re.sub(r'\s+', ' ', input_text)

    if prompt is None:
        prompt = f"<s> [INST] Paraphrase the following text. If sections are repeated, simply mention the paraphrase once in the output text.\nOriginal: {input_text}\nParaphrase: [/INST]"
    else:
        prompt = f"<s> [INST] {prompt}\nOriginal: {input_text}\nParaphrase: [/INST]"

    if mode == "strict":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': num_output_tokens, 'max_time': 60.0,
                         'num_beams': 3}
    elif mode == "variable":
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': num_output_tokens, 'max_time': 60.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 3, 'do_sample': True,
                         'top_p': 0.92, 'temperature': 0.6}

    else:
        configuration = {'return_full_text': False, 'num_return_sequences': 1,
                         'max_new_tokens': num_output_tokens, 'max_time': 60.0,
                         'no_repeat_ngram_size': 3, 'num_beams': 3, 'do_sample': True,
                         'top_p': 0.92, 'temperature': 0.6}

    query = ["", "", "mistralai/Mixtral-8x7B-Instruct-v0.1", prompt, configuration]
    (success, return_text) = query_text_generation(query, endpoint, headers)
    if success:
        return remove_words_after_last_dot(return_text)

    print(return_text)
    return ""

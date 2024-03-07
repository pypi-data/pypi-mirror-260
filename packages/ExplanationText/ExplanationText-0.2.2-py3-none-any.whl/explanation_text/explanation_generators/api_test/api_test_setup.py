import random

from explanation_text.explanation_generators.explanation_generator_v1.sentence_construction import generate_explanation_with_sentence_construction


def get_run_configuration(single_object):
    prompt = generate_explanation_with_sentence_construction(single_object)
    if 'parts' in single_object:
        for part in single_object['parts']:
            connection = random.choice(["very strongly", "strongly", "weakly", "very weakly"])
            prompt += (f"{part['part:label']} is {connection} connected to " + single_object['label'] + ". ")

    # Text Generation
    rephrase_models = ["prithivida/parrot_paraphraser_on_T5", "ramsrigouthamg/t5_sentence_paraphraser"]
    rephrase_config = {'num_return_sequences': 3, 'min_new_tokens': 250, 'no_repeat_ngram_size': 3,
                       'max_time': 120.0, 'num_beams': 3, 'do_sample': True, 'top_k': len(prompt),
                       'top_p': 0.9, 'temperature': 0.9}
    rephrase_prompt = prompt

    text_gen_models = ["bigscience/bloom", "EleutherAI/gpt-neox-20b"]
    text_gen_config = {'return_full_text': False, 'num_return_sequences': 3,
                       'max_new_tokens': len(prompt), 'no_repeat_ngram_size': 3, 'max_time': 120.0,
                       'num_beams': 3, 'do_sample': True, 'top_k': len(prompt),
                       'top_p': 0.9, 'temperature': 0.9}
    text_gen_prompt = "Rephrase the sentence. Sentence: " + prompt + " Rephrase:"

    assistant_models = ["OpenAssistant/oasst-sft-1-pythia-12b"]
    assistant_config = {'return_full_text': False, 'num_return_sequences': 1,
                        'max_new_tokens': len(prompt), 'no_repeat_ngram_size': 1, 'max_time': 120.0,
                        'num_beams': 1, 'do_sample': True, 'top_k': len(prompt),
                        'top_p': 0.9, 'temperature': 0.9}
    assistant_prompt = "<|prompter|>Paraphrase the following sentence: " + prompt + ".<|endoftext|><|assistant|>"

    rephrase_test = ["TG_A", rephrase_models, ["text-generation"],
                     [rephrase_prompt, rephrase_prompt, rephrase_prompt], rephrase_config]
    text_gen_test = ["TG_B", text_gen_models, ["text-generation"],
                     [text_gen_prompt, text_gen_prompt, text_gen_prompt], text_gen_config]
    assistant_test = ["TG_C", assistant_models, ["text-generation"],
                      [assistant_prompt, assistant_prompt], assistant_config]

    # Summarization
    summarization_models = ["facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6",
                            "philschmid/bart-large-cnn-samsum",
                            "moussaKam/barthez-orangesum-abstract", "google/pegasus-cnn_dailymail",
                            "google/pegasus-xsum", "google/bigbird-pegasus-large-bigpatent",
                            "csebuetnlp/mT5_multilingual_XLSum",
                            "pszemraj/led-base-book-summary", "slauw87/bart_summarisation",
                            "google/pegasus-large"]
    summarization_config = {'min_length': round(len(prompt) * 0.75),
                            'max_length': round(len(prompt) * 1.25),
                            'max_time': 120.0}
    summarization_prompt = prompt
    summarization_test = ["SUM", summarization_models, ["summarization"],
                          [summarization_prompt], summarization_config]

    tests = [rephrase_test, text_gen_test, assistant_test, summarization_test]

    return tests


demoSample = []


def get_parts():
    pass


# ---- Examples for tasks -----

# Test Fill Mask (has to contain [MASK]
test_b_models = ["microsoft/deberta-base", "bert-base-uncased"]
test_b_tasks = ["fillMask"]
test_b_prompts = []
# for sample in demoSample:
    # test_b_prompts.extend([f"The Objects {get_parts(sample, 2)} are [MASK]."])
test_b_configuration = {}
test_b = ["FillMask_Test_", test_b_models, test_b_tasks, test_b_prompts, test_b_configuration]

# Test Conversational (Each prompt will is next conversation piece)
test_c_models = ["microsoft/DialoGPT-large"]
test_c_tasks = ["conversational"]
test_c_prompts = []
for sample in demoSample:
    test_c_prompts.extend(
        [f"An image was classified by a neural network as a {sample.get('main_label')}. Explain the classification.",
         "How did you came up with this explanation?"])
test_c_configuration = {"max_time": 120.0}
test_c = ["Conversational_", test_c_models, test_c_tasks, test_c_prompts, test_c_configuration]

# Test Summarization (empty configuration)
test_d_models = ["facebook/bart-large-cnn", "philschmid/bart-large-cnn-samsum"]
test_d_tasks = ["summarization"]
test_d_prompts = []
for sample in demoSample:
    test_d_prompts.extend([f"An image was classified by a neural network as a {sample.get('main_label')}. The reason "
                           f"for this classification is ",
                           f"Image Classification of {sample.get('main_label')} with neural networks work the "
                           f"following way"])
test_d = ["Summarization_", test_d_models, test_d_tasks, test_d_prompts, {}]

runTest = [test_b, test_c, test_d]

# ---- End of Examples-----

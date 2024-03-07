import os
import re
import string

import inflect
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

knowledge_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'countries/')

PRINT_KNOWLEDGE_BASE_INFOS = False


def get_prefiltered_information(location, part, similarity_threshold=0.6, max_text_length=200):
    part_synonyms = get_synonyms(part, similarity_threshold)
    part_synonyms.append(part)
    part_synonyms_variants = generate_word_variants(part_synonyms)

    all_variants = [*part_synonyms, *part_synonyms_variants]

    if PRINT_KNOWLEDGE_BASE_INFOS:
        print("   Variants for part " + part + ": " + str(part_synonyms_variants))
    full_location_text = get_full_information_of_country(location)
    return filter_and_sort_sentences(full_location_text, all_variants, max_text_length)


def get_full_information_of_country(country):
    try:
        with open(os.path.join(knowledge_base_path + country.lower().replace(" ", "_") + ".txt"), 'r',
                  encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Country {country} wasn't found in knowledge base.")
        return ""


def get_synonyms(word, similarity_threshold):
    synonyms = set()
    word_synsets = wordnet.synsets(word, pos=wordnet.NOUN)

    # Map some additional synonyms to align with the knowledge base
    class_mapping = {
        "car": ["vehicle"],
        "truck": ["vehicle", "car"],
        "vehicle": ["car", "truck"],
        "road": ["street"],
        "side_walk": ["sidewalk", "path", "footpath"],
        "cross_walk": ["crosswalk", "footpath"],
        "barrier": ["guardrail", "bollard"],
        "building": ["house"],
        "house": ["building"],
        "person": ["pedestrian"],
        "vegetation": ["plant", "grass", "bush", "tree", "greenery"],
        "tree": ["vegetation", "plant", "bush", "greenery"],
        "text": ["letters", "script", "writing", "characters"],
    }
    if word in class_mapping:
        synonyms.update(class_mapping[word])

    # filter out similar synonyms by threshold
    for syn in word_synsets:
        for lemma in syn.lemmas():
            synonym = lemma.name()
            synonyms.add(synonym)

            similarity = max(word_synsets[0].wup_similarity(wordnet.synsets(synonym)[0]) for syn in word_synsets)
            if similarity is not None and similarity >= similarity_threshold:
                synonyms.add(synonym)

    return list(synonyms)


def generate_word_variants(words):
    p = inflect.engine()

    def get_unique_variants(word):
        variants = set()

        # Process each part of the compound word individually
        for part in re.split(r'[\s\-_]', word):
            part = part.lower()  # Use lowercase for consistency
            variants.add(part)
            variants.add(p.plural(part))
            variants.add(p.singular_noun(part) or part)
            variants.add(p.plural_noun(part))
            variants.add(p.a(part))
            variants.add(p.an(part))
            variants.add(p.ordinal(part))
            variants.add(p.present_participle(part))

        return variants

    # Generate variants for each word and flatten the list
    all_variants = [variant for word in words for variant in get_unique_variants(word)]

    # Remove duplicates and return the result
    return list(set(all_variants))


def filter_and_sort_sentences(text, words, max_length):
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    sentence_word_count = []

    for sentence in sentences:
        sentence_without_punctuation = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence_words = sentence_without_punctuation.split()
        word_count = sum(1 for word in sentence_words if word.lower() in words)
        if word_count > 0:
            sentence_word_count.append((sentence, word_count))
    sorted_sentences = sorted(sentence_word_count, key=lambda x: x[1], reverse=True)

    result_sentences = []
    current_length = 0
    for sentence, _ in sorted_sentences:
        if current_length + len(sentence) <= max_length:
            result_sentences.append(sentence + ". ")
            current_length += len(sentence) - 1
        else:
            break
    for sentence, _ in sorted_sentences:
        subsequent_sentence = sentences[sentences.index(sentence) + 1]
        if current_length + len(subsequent_sentence) <= max_length:
            result_sentences.append(subsequent_sentence + ". ")
            current_length += len(subsequent_sentence)
        else:
            break

    result_text = ' '.join(result_sentences)

    return result_text

# Test for run without whole pipeline
# knowledge_base_path = "countries/"
# print(get_prefiltered_information("brazil", "car"))
# print(get_prefiltered_information("germany", "road"))
# print(get_prefiltered_information("peru", "house"))
# print(get_prefiltered_information("spain", "traffic_light"))

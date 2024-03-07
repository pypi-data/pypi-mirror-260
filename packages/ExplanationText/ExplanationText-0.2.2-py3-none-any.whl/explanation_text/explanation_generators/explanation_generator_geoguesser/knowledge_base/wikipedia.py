import wikipediaapi

MAX_LENGTH_WIKIPEDIA = 250


def get_first_sentence_wikipedia(article):
    wiki_wiki = wikipediaapi.Wikipedia("geoguesser_knowledge_base/0.1", extract_format=wikipediaapi.ExtractFormat.WIKI)
    wiki_wiki._user_agent = "geoguesser_knowledge_base/0.1"
    page_py = wiki_wiki.page(article)
    if not page_py.exists():
        return f"Wikipedia article for {article} not found."

    filtered_text = remove_text_inside_brackets(page_py.summary)
    first_sentence = extract_text_until_last_period(filtered_text, MAX_LENGTH_WIKIPEDIA)
    return " " + first_sentence


def remove_text_inside_brackets(text):
    result = ""
    inside_brackets = 0

    for char in text:
        if char == '(':
            inside_brackets += 1
        elif char == ')':
            inside_brackets -= 1
        elif inside_brackets == 0:
            result += char

    return result.strip() + "."


def extract_text_until_last_period(text, max_length):
    if max_length < len(text):
        text = text[:max_length]
        last_period_position = text.rfind('.')
        result_text = text[:last_period_position + 1]

        return result_text
    else:
        return text

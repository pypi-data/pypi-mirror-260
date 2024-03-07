import json
import requests


def query_text_generation(query, endpoint, headers):
    """
    Function to process Query for tasks text-generation and text2Text
    """
    payload = {
        "inputs": query[3],
        "parameters": query[4],
        "options": {"wait_for_model": True}
    }
    data = json.dumps(payload)
    response_list = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    try:
        response_list = json.loads(response_list.content.decode("utf-8"))
    except:
        return False, [str(response_list)]

    if isinstance(response_list, list):
        explanation = response_list[0]['generated_text'].replace('\n', ' ').replace('\r', '')
        return True, explanation

    return False, [str(response_list)]


def query_fill_mask(query, endpoint, headers):
    """
    Function to process Query for task fillMask
    Inputs have to contain [MASK] keyword and no parameters can be set
    """
    payload = {
        "inputs": query[3],
        "options": {"wait_for_model": True}
    }
    data = json.dumps(payload)
    response_list = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    response_list = json.loads(response_list.content.decode("utf-8"))

    if isinstance(response_list, list):
        parsed_response = []
        for response in response_list:
            explanation = f"Token/Score: {response[0]['token_str']}/{response[0]['score']}, {response[0]['sequence']}"
            parsed_response.append("     " + explanation.replace('\n', ' ').replace('\r', ''))
        return True, parsed_response

    return False, [str(response_list)]


def query_summarization(query, endpoint, headers):
    """
    Function to process Query for task summarization
    """

    parameters = query[4]
    parameters['do_sample'] = False
    payload = {
        "inputs": query[3],
        "parameters": parameters,
    }
    data = json.dumps(payload)
    response_list = requests.request("POST", endpoint + query[2], headers=headers, data=data)
    response_list = json.loads(response_list.content.decode("utf-8"))

    if isinstance(response_list, list):
        parsed_response = []
        for response in response_list:
            explanation = response['summary_text']
            parsed_response.append("     " + explanation.replace('\n', ' ').replace('\r', ''))
        return True, parsed_response

    return False, [str(response_list)]


def query_conversational(query, endpoint, headers):
    """
    Function to process Query for tasks conversational
    Each prompt will be passed to model sequentially
    """
    parsed_response = []
    past_user_inputs = []
    generated_responses = []

    for prompt in query[3]:
        inputs = {
            "past_user_inputs": past_user_inputs,
            "generated_responses": generated_responses,
            "text": prompt
        }

        payload = {
            "inputs": inputs,
            "parameters": query[4],
            "options": {"wait_for_model": True}
        }

        data = json.dumps(payload)
        response = requests.request("POST", endpoint + query[2], headers=headers, data=data)
        response = json.loads(response.content.decode("utf-8"))

        if 'conversation' in response and 'generated_text' in response:
            explanation = response['generated_text']
            parsed_response.append("     '" + prompt + "' -> "
                                  + explanation.replace('\n', ' ').replace('\r', ''))
            past_user_inputs = response['conversation']['past_user_inputs']
            generated_responses = response['conversation']['generated_responses']
        else:
            return False, [str(response)]

    return True, parsed_response


def get_parts(input_sample, max_parts):
    """
    Help Function to get a string or part_labels with given maximum number of parts
    """
    return_value = ""
    if 'parts' in input_sample:
        parts = input_sample.get('parts')
        count = 0

        # For each part
        for part in parts:
            # should key be 'part_label' or 'partLabel'?
            part_label = part.get('part_label')

            # add part label
            if count < max_parts:
                return_value += str(part_label) + ", "
            count += 1

        # Add 'and' instead of last comma
        return_value = return_value[:-2]
        if len(parts) > 1:
            last_comma_index = return_value.rfind(",")
            return_value = (return_value[:last_comma_index]
                           + " and" + return_value[last_comma_index + 1:])

    return return_value


def init_models(api_token):
    """
    Sends "Hello World" Request to HuggingFace to load models
    """
    endpoint = "https://api-inference.huggingface.co/models/"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
    configuration = {}

    # Initialize model for rephrasing and information generator
    prompt = "<s>[INST] Hello World[/INST]</s>"
    query = ["", "", "mistralai/Mixtral-8x7B-Instruct-v0.1", prompt, configuration]
    query_text_generation(query, endpoint, headers)

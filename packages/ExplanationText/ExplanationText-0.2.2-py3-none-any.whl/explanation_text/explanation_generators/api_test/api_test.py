import csv
import os
import random
from datetime import datetime
from explanation_text.explanation_generators.api_utils import query_text_generation, \
    query_fill_mask, query_summarization, query_conversational
from explanation_text.explanation_generators.api_test.api_test_setup import get_run_configuration

# Configuration

# ---- Add your own API Token --------
API_TOKEN = "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"

RETRY_LIMIT = 5
ENDPOINT = "https://api-inference.huggingface.co/models/"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_TOKEN}"}


def generate_explanation_with_api_test(single_object):
    """
    Main function to run API Tests to HuggingFace.co
    Set up your tests to run in the 'EDIT HERE' Section and set your personal APIToken from HuggingFace above
    Models: List of models from HuggingFace, all tasks and prompts will be run for each given model
    Implemented tasks: 'text-generation', 'text2text' (same API), 'fillMask', 'summarization' and 'conversational'
    Prompts: Multiple Prompts can be set for each sample (Object in image), format defined in README
             to get a String of parts, use function 'getParts' with parameter for number of parts
    Configuration: A JSON Object containing the parameters defined in the API description, different for each task
    Documentation: https://huggingface.co/docs/api-inference/detailed_parameters#summarization-task

    Different Examples for each task can be found in 'APITestUtils'
    """

    run_test = get_run_configuration(single_object)

    # Append queries for each test
    queries = []
    for test in run_test:
        queries.extend(generate_requests_for_test(test))

    # Start Requests to API, sort by id and return explanations
    responses, rows = start_api_queries(queries)
    write_to_csv(rows)
    responses.sort()
    return_value = []
    for response in responses:
        return_value.append(
            f"  -- Explanations for {response[0][0]} with task {response[0][1]} and model {response[0][2]} -- ")
        return_value.append(response[1])
        return_value.append("")
    return return_value


def generate_requests_for_test(test):
    """
    Function to generate Query objects for each test for each combination of models and tasks
    """
    test_name = test[0]
    models = test[1]
    tasks = test[2]
    prompts = test[3]
    configuration = test[4]
    identifier_count = 0
    queries = []
    for model in models:
        for task in tasks:
            for prompt in prompts:
                queries.append([test_name + str(identifier_count), task, model,
                                prompt, configuration, RETRY_LIMIT])
                identifier_count += 1

    return queries


def start_api_queries(queries):
    """
    Function to run a set of queries
    They are organized in a pool, run a random query until its finished or failed
    Each query has a given set of tries until its discarded
    Returns a list of explanations and a list of rows for the output file
    """

    done_requests = 1
    request_size = len(queries)
    explanations = []

    # Initialize rows for csv file
    rows = []

    while len(queries) > 0:
        # Shuffle Queries and pick one
        random.shuffle(queries)
        query = queries.pop()

        print(f"-- {done_requests} / {request_size} Start processing query with id {query[0]} --")
        (success, explanation) = process_query(query)

        # Get explanation on success or put it back to the pool on failure
        if not success:
            query[5] = query[5] - 1
            if query[5] <= 0:
                print(f"-- Request with id {query[0]} failed, too many tries --")
                print(f"   Response: {explanation}")
                explanations.append((query, explanation))
                done_requests += 1
            else:
                queries.append(query)
        else:
            explanations.append((query, explanation))
            rows.append({"id": query[0], "task": query[1], "model": query[2], "prompt": query[3],
                         "explanation": explanation, "configuration": query[4]})
            done_requests += 1

    return explanations, rows


def process_query(query):
    """
    Function to process a single query
    Calls individual functions for different tasks
    """

    print(f"-- Process query {query[0]} with task {query[1]} and model {query[2]} --")
    if query[1].lower() == "text-generation" or query[1].lower() == "text2text":
        return query_text_generation(query, ENDPOINT, HEADERS)
    if query[1].lower() == "fillmask":
        return query_fill_mask(query, ENDPOINT, HEADERS)
    if query[1].lower() == "summarization":
        return query_summarization(query, ENDPOINT, HEADERS)
    if query[1].lower() == "conversational":
        return query_conversational(query, ENDPOINT, HEADERS)

    return (False,
                [f"  Query with id {query[0]} failed because task {query[1]} is not implemented"])


def write_to_csv(rows, output_path="output"):
    print("Writing API-Test into csv file..")
    now = datetime.now()
    filename = now.strftime("API_Test_%d%m%Y_%H%M%S")
    if not os.path.exists(output_path):
        print("Directory for output " + str(output_path) + " does not exist")
        os.makedirs(output_path)
        print("New output directory is created")
    file_path = os.path.join(output_path, filename + ".csv")
    with open(file_path, 'x') as f:
        # write rows to csv file
        writer = csv.DictWriter(f, fieldnames=["id", "task", "model", "prompt",
                                               "explanation", "configuration"])
        writer.writeheader()
        writer.writerows(rows)
    print("API-Test written into file " + str(filename))

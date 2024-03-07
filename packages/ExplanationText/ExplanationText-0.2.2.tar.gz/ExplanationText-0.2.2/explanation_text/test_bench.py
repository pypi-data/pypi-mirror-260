import json
from datetime import datetime
from explanation_generator_main import ExplanationGenerator
from explanation_text import init_models


class TestBench:
    """
    A testbench class that reads data from a file and provides a testData method to
    test the ExplanationText implementation automatically
    """

    def __init__(self, input_folder_path, token_path, mode="ExplanationGeneratorV1",
                 output_path="output"):
        """
        Constructor for the testbench class, calls read_data method and sets in- and output folder paths
        """
        self.folder_path = input_folder_path
        self.output_path = output_path
        self.mode = mode
        self.mode_description = str(self.mode)
        self.api_token = ""
        self.google_api_token = ""
        self.load_api_keys_from_file(token_path)

    def load_api_keys_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if "huggingface_api_key" in data and "google_vision_api_key" in data:
                    self.api_token = data.get("huggingface_api_key")
                    self.google_api_token = data.get("google_vision_api_key")
                else:
                    print("Error: The file should contain exactly two password key-value pairs.")
                    return None
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{file_path}': {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate_explanations(self, parsed_test_data):
        explanation_generator = ExplanationGenerator(mode=self.mode, api_token=self.api_token,
                                                     google_api_token=self.google_api_token)
        print("Init HuggingFace Language Models")
        init_models(self.api_token)
        print("\nStart testing samples with mode " + str(self.mode_description))

        explanations = []
        average_times = []
        print(f"Testing {len(parsed_test_data)} samples")
        for test_sample in parsed_test_data:
            explanation, average_time = explanation_generator.generate_explanation(test_sample, return_time=True)
            print(json.dumps(explanation, indent=4, ensure_ascii=False))
            print("")
            explanations.append(explanation)
            average_times.append(average_time)

        total_average_time = round(sum(average_times) / len(average_times), 2)
        print(f"All samples tested with an total average of {str(total_average_time)} seconds per object")
        return explanations

    def remove_img_data_from_json(self, file_path):
        full_path = self.folder_path+"/"+file_path
        print("Clear file "+full_path+" from image data")
        try:
            with open(full_path, 'r') as file:
                data = json.load(file)

            # Update the values for "img" and "heatmap" keys to "base64"
            data['img'] = 'base64'
            data['heatmap'] = 'base64'
            # Check if "heatmap" key is within a list of JSON objects
            for obj in data.get('objects', []):
                if 'heatmap' in obj:
                    obj['heatmap'] = 'base64'
                obj['segmentation'] = ""
                obj['segmentation_and_relevancies'] = ""
                obj['merged_segmentation_and_relevancies'] = ""
                obj['mask'] = ""
                obj['xaimap'] = ""

                for part in obj.get('parts', []):
                    part['img'] = 'base64'
                    part['mask'] = ""

            # Convert the updated JSON data to a string
            updated_json_str = json.dumps(data, indent=2)

            # Save the changes back to the file
            with open(full_path, 'w') as file:
                file.write(updated_json_str)

            print(f'Successfully updated and saved the JSON file: {file_path}')

        except FileNotFoundError:
            print(f'Error: File not found - {file_path}')
        except json.JSONDecodeError:
            print(f'Error: Invalid JSON format in file - {file_path}')
        except Exception as e:
            print(f'Error: {e}')

    def test_json_file(self, file_path, write_to_file):
        """
        Method to test explanation generator with json file
        """

        try:
            with open(self.folder_path+"/"+file_path, 'r') as file:
                data = json.load(file)
                # generate explanations
                explanations = []
                explanations.extend(["--- Explanations for Mode: " + self.mode_description + " ---"])
                explanations.extend(self.generate_explanations([data]))

                # write in output file
                if write_to_file:
                    print("Writing into output file..")
                    now = datetime.now()
                    filename = now.strftime("explanation_%d%m%Y_%H%M%S")
                    self.write_output(explanations, filename)
                    print("Explanations written into file " + str(filename))

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding the JSON file '{file_path}': {e}")

    def test_json_file_fallback_comparision(self, file_path):
        """
        Method to test individual explanation functions
        """

        explanation_generator = ExplanationGenerator(mode=self.mode, api_token=self.api_token,
                                                     google_api_token=self.google_api_token)

        try:
            with open(self.folder_path+"/"+file_path, 'r') as file:
                data = json.load(file)
                # generate explanations
                print("Start generating explanations")
                overview_text = explanation_generator.generate_overview_gg(data)
                medium_text_fallback = explanation_generator.generate_medium_gg(data, fallback=True)
                detailed_text_fallback = explanation_generator.generate_detailed_gg(data, fallback=True)
                medium_text = explanation_generator.generate_medium_gg(data)
                detailed_text = explanation_generator.generate_detailed_gg(data)

                # print results
                print("=== Overview Explanation ===")
                print(overview_text)

                print("=== Explanations with fallback on =====")
                print(medium_text_fallback)
                print(detailed_text_fallback)

                print("=== Explanations without fallback on =====")
                print(medium_text)
                print(detailed_text)

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding the JSON file '{file_path}': {e}")


# TestBench Demo
testBench = TestBench('test_data', "api_keys.json", mode="ExplanationGeneratorGG")

# add new test data filenames here
example_data_files = ["argentina.json", "australia.json", "colombia.json", "france.json", "germany.json", "greece.json",
                      "india.json", "mexico.json", "mongolia.json", "nigeria.json", "singapore.json",
                      "south_africa.json", "sweden.json", "uruguay.json", "usa.json", "demos/geoguesser_demo.json"]

eval_files = ["eval_inputs/colombia.json", "eval_inputs/germany.json", "eval_inputs/greece.json",
              "eval_inputs/mexico.json", "eval_inputs/mongolia.json", "eval_inputs/nigeria.json",
              "eval_inputs/singapore.json", "eval_inputs/south_africa.json", "eval_inputs/uruguay.json",
              "eval_inputs/usa.json"]

# clear img data from test files if necessary
for file in eval_files:
    testBench.remove_img_data_from_json(file)
# testBench.remove_img_data_from_json(example_data_files[0])

# run test by setting index
# testBench.test_json_file_fallback_comparision(example_data_files[4])


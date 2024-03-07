from google.cloud import vision

from explanation_text.explanation_generators.explanation_generator_geoguesser.knowledge_base.wikipedia import \
    get_first_sentence_wikipedia


def detect_landmark(part_label, image_data, api_key):
    if api_key != "":

        client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
        image = vision.Image(content=image_data)

        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        print("Landmarks:")

        if landmarks:
            landmark = landmarks[0].description
            print("  ! Landmark {0} detected.".format(landmark))
            part_information = "The {0} was detected as {1}.".format(part_label, landmark)
            part_information += get_first_sentence_wikipedia(landmark)
            return part_information + " "
        else:
            print(response)
            print("  ! No Landmark detected.")
            return ""

    print("ERROR: No API Key for google vision api set")
    return ""

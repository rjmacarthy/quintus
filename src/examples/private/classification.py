import json
import glob

from quintus import Quintus

quintus = Quintus()


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def classify_document(document, options, examples=[]):
    model_output = quintus.classify(document, options, examples)
    return model_output


classifications = []


def glob_json_files():
    files = glob.glob("../data/*.json")
    for file in files:
        data = load_json(file)
        print(f"Classifying file: {data['title']}")
        title = data["title"]
        body = quintus.processor.html_to_text(data["body"])[:500]
        classification = classify_document(
            f"{title} - {body}",
            ["normal support document", "cryptocurrency description"],
        )
        print(f"Classified as: {classification}")
        classifications.append(
            {"id": data["id"], "title": data["title"], "classification": classification}
        )

    if len(classifications) > 0:
        print("Writing classifications to file...")
        write_classifications_to_file(classifications)


def write_classifications_to_file(classifications):
    with open("../data/classifications.json", "w") as f:
        json.dump(classifications, f)


glob_json_files()

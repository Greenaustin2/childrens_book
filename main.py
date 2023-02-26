import os
import openai
import json
from pathlib import Path
from base64 import b64decode
from textblob import TextBlob
import pprint
import requests


new_folder_name = "00014"
API_KEY = "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"
openai.api_key = API_KEY
NEW_DIRECTORY = Path.cwd() / "drafts" / new_folder_name
DATA_DIR = Path.cwd() / "drafts" / new_folder_name / "responses"
JSON_FILE = DATA_DIR / "1676495172.json"
TEXT_DIR = Path.cwd() / "drafts" / new_folder_name / "text"
IMAGE_DIR = Path.cwd() / "drafts" / new_folder_name / "images"
NEW_DIRECTORY.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
TEXT_DIR.mkdir(exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


sizes = {"small": "256x256", "medium": "512x512", "large": "1024x1024"}
mediums = ["high definition photo", "crayon drawing", "watercolor painting", "colored pencil drawing", "marker drawing", "line drawing"]
references = ["goodnight moon", "corduroy", "the giving tree", "dr. seuss", "shel silverstein", "eric carle"]


def convert_image(file_name):
    global JSON_FILE
    JSON_FILE = DATA_DIR / file_name
    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)


def generate_image(prompt, number):
    response = openai.Image.create(
        prompt=prompt,
        n=number,
        size=sizes["large"],
        response_format="b64_json"
    )
    file_name = DATA_DIR / f"{response['created']}.json"
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump(response, file)


def text_completion(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=.5,
        n=1,
        max_tokens=2048
    )
    file_name = TEXT_DIR / f"{response['created']}.txt"
    story = response["choices"][0]["text"]
    with open(file_name, mode='w') as text_file:
        text_file.write(story)
    text_list = [sentence for sentence in story.split("\n") if sentence != ""]
    return text_list
    # with open(Path.cwd() / "text" / f"{response['created']}") as f:
    #     text_list = [sentence for sentence in f.read().split("\n") if sentence != ""]
    #     return text_list


image_query = f"a {mediums[0]} drawing of a young child and a huge crayon in the style of {references[4]}"
text_query = "a 3 paragraph childrens story about a nameless parakeet that dreams of being a jazz musician, and directly below each paragraph there is a seperate short description of an image representing what is happening in that paragraph. do not label the paragraphs or image descriptions"

text = text_completion(text_query)

for item in range(1, len(text), 2):
    # blob = TextBlob(item)
    # print(blob.noun_phrases)
    text_prompt = f"{text[item]}, {mediums[0]}"
    # print(text_prompt)
    # generate_image(prompt=text_prompt, number=1)
    generate_image(prompt=text_prompt, number=1)

directory = os.listdir(f'/users/austingreen/PycharmProjects/childrens_book/drafts/{new_folder_name}/responses')
for file in directory:
    if file.endswith(".json"):
        convert_image(file)


# generate image descriptions separately for each paragraph to avoid formatting errors
#   generate random choice from lsit of nouns and story points/pot points?

# for item in text:
#     query = f"description of an image representing what is going on in this paragraph "{item}"
#     text_completion(query)




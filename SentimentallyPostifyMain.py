from flask import Flask, render_template, url_for, request, flash
import os
import io

# # Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
import PIL.Image as Image

import torch
import torchtext
from torchtext.datasets import text_classification
import torch.nn as nn

import torch.nn.functional as F
from torch.utils.data import DataLoader
import time
from torch.utils.data.dataset import random_split
NGRAMS = 2
BATCH_SIZE = 16

# Set up credentials for Vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

# Instantiates a client for Vision
client = vision.ImageAnnotatorClient()

# Class for the model
class TextSentiment(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()
        
    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

# Labels
import re
from torchtext.data.utils import ngrams_iterator
from torchtext.data.utils import get_tokenizer

ag_news_label = {1 : "Company",
                2 : "EducationalInstitution",
                3 : "Artist",
                4 : "Athlete",
                5 : "OfficeHolder",
                6 : "MeanOfTransportation",
                7 : "Building",
                8 : "NaturalPlace",
                9 : "Village",
                10 : "Animal",
                11: "Plant",
                12: "Album",
                13: "Film",
                14: "WrittenWork"}

# Inference ability added here
def predict(text, model2, vocab, ngrams):
    tokenizer = get_tokenizer("basic_english")
    with torch.no_grad():
        text = torch.tensor([vocab[token]
                            for token in ngrams_iterator(tokenizer(text), ngrams)])
        output = model2(text, torch.tensor([0]))
        return output.argmax(1).item() + 1

#imports for facebook
import json
import facebook

# Init for Facebook API
token = {""}
graph = facebook.GraphAPI(token)
groups = []
names = []
descriptions = []
emails = []

matching_groups = []

def findgroup():
    fields = {'groups'}

    profile = graph.get_object('me', fields = fields)

    for object in profile["groups"]["data"]:
        groups.append(object["id"])
        find_description(object["id"])

def findpost():
    for id in groups:
        print(id)

def find_description(id):
    profile = graph.get_object(id, fields = 'name, email, description')

    names.append(profile["name"])
    emails.append(profile["email"])
    #descriptions.append(profile["description"])

def find_match(image_category, model2, vocab):
    image_and_group_matches = []
    # for i in range(len(groups)):
    for i in range(5):
        group_category = "%s" %ag_news_label[predict(names[i], model2, vocab, 2)]
        temp = str(i)
        temp += group_category
        print(temp)
        if(group_category == image_category):
            image_and_group_matches.append(groups[i])
    return image_and_group_matches

# setting up flask for web interface
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

name = ""

@app.route("/")
def home():
    return render_template('index.html', title='FaceBook Hackathon')

@app.route("/", methods=['POST'])
def upload():
    name = request.form['Title']
    target = os.path.join(APP_ROOT, 'images\\')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = target + filename
        print(destination)
        file.save(destination)
        return recognize(filename, target)

def recognize(name, path):
    # #Identifies the file and file path
    FILE_NAME = name
    FOLDER_PATH = path

    # #Loads the image into the memory
    with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)

    # # Performs text detection on the image file
    responseText = client.text_detection(image=image)

    image_text = ""

    texts = responseText.text_annotations
    print('Text:')

    for i in range(len(texts)):
        if (i != 0):
            image_text += texts[i].description
            image_text += " "

    print(image_text)

    # Dataset loading
    if not os.path.isdir('./.data'):
        os.mkdir('./.data')
    train_dataset, test_dataset = text_classification.DATASETS['DBpedia'](
        root='./.data', ngrams=NGRAMS, vocab=None)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Model creation with dataset
    VOCAB_SIZE = len(train_dataset.get_vocab())
    EMBED_DIM = 32
    NUN_CLASS = len(train_dataset.get_labels())
    model2 = TextSentiment(VOCAB_SIZE, EMBED_DIM, NUN_CLASS).to(device)

    # Loading state_dict from model 1 to access pretrained information
    model2.load_state_dict(torch.load('model_save.pt'))
    model2.eval()

    vocab = train_dataset.get_vocab()
    model2 = model2.to("cpu")

    image_category = "%s" %ag_news_label[predict(image_text, model2, vocab, 2)]

    # Now the facebook stuff starts
    findgroup()
    findpost()
    i = 0

    for name in names:
        print(name)

    matching_groups = find_match(image_category, model2, vocab)
    
    answer = "The image is classified by vision as "
    answer += image_category
    answer += " and the matching groups are "

    if(len(matching_groups) >= 1):
        for i in range(len(matching_groups)):
            profile = graph.get_object(matching_groups[i], fields = 'name, email, description')
            print(profile["name"])
            answer += profile["name"]
            answer += " "
            graph.put_photo(image=open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb'), message='Facebook AI Hackathon Sample Post', album_path=matching_groups[i] + "/photos")

    # graph.put_photo(image=open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb'), message='commute methods with travel', album_path=groups[0] + "/photos")

    return answer

if __name__ == '__main__':
    app.run(debug=True)
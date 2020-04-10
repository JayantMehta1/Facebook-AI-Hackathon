# Imports for Flask and Python Scripts
from flask import Flask, render_template, url_for, request, flash, jsonify, make_response
import os
import io

# Imports the Google Cloud client library including the Vision API
from google.cloud import vision
from google.cloud.vision import types
import PIL.Image as Image

# Imports for PyTorch
import torch
import torchtext
from torchtext.datasets import text_classification
import torch.nn as nn

import torch.nn.functional as F
from torch.utils.data import DataLoader
import time
from torch.utils.data.dataset import random_split

# NGRAMS determine how many words per reading there are/repeated transfer words (the way strings are parced)
# e.g., "There were multiple cars in the parking lot" => "There were, were multiple, multiple cars, etc.")
NGRAMS = 2
BATCH_SIZE = 16

# Set up credentials for Vision
# Please use your own credentials as a json file
# Name it "ServiceAccountToken.json" and add it in the "flaslbackend" folder within this project to use Google Vision
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'flaskbackend/ServiceAccountToken.json'

# Instantiates a client for Vision
#client = vision.ImageAnnotatorClient()

# Class for the model using PyTorch
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

# These are the different category labels that can be used for this project
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
# token = "Filled by Facebook Login AJAX Post Request"
# graph = facebook.GraphAPI(token)

# Stores the id of each group
groups = []

#Stores the name of each group
names = []

#Stores the description of each group
descriptions = []

emails = []

#Stores the groups that match with the image category
matching_groups = []

def findgroup(fb_graph):
    graph = fb_graph
    fields = {'groups'}

    profile = graph.get_object('me', fields = fields)

    for object in profile["groups"]["data"]:
        groups.append(object["id"])
        find_description(object["id"], graph)

def findpost(fb_graph):
    graph = fb_graph
    for id in groups:
        print(id)

def find_description(id, fb_graph):
    graph = fb_graph
    profile = graph.get_object(id, fields = 'name, email, description')

    print("For " + id + ", the profile is")
    print(profile)
    
    names.append(profile["name"])
    emails.append(profile["email"])
    descriptions.append(profile["description"])

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

# setting up flask back-end server for web interface
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

name = ""

@app.route("/")
def home():
    return render_template('index.html', title='FaceBook Hackathon', token='Hello, this is React and Flask Combo')

# This POST Request to Flask is used to access the token with all the required permissions from Facebook Login
@app.route('/', methods=['GET', 'POST'])
def start():
    # POST request
    if request.method == 'POST':
        print('Incoming data from React Facebook Login')
        print("The data type of this request is a JSON:" + str(request.is_json))
        if(request.is_json):
            # parse access token as a JSON
            access_token_JSON = request.get_json(force=False,silent=False,cache=True)
            # Gets the value of the key : value pair in JSON (which is the token)
            temp_token = str(access_token_JSON['facebook_access_token'])
            print(temp_token)

            # Just communicates to the JavaScript Console that this data has been accessed
            validation = make_response('Thank you. The access token has been received', 200)
            # Stores the token data using browser cookies so data is not wiped every time there is a new post request
            validation.set_cookie(
                 "facebook_access_token", 
                 value = temp_token # ,
                #  max_age = 300,
                #  expires = None,
                #  path = request.path,
                #  domain = None,
                #  secure = False,
                #  httponly = False,
                #  samesite = False
                 )
            return validation
        else:
            # This POST Request to Flask is to submit the image and then post on Facebook Groups using AI
            
            # @app.route("/", methods=['POST'])
            # def process():
            cookies = request.cookies

            fb_token = cookies.get("facebook_access_token")

            print("the token: ")
            print(fb_token)
            # Gets the name of the form
            name = request.form['Title']

            # One option is to pass in the token through this form
            my_test_token = request.form['Access Token']
            print(my_test_token)

            target = os.path.join(APP_ROOT, 'images\\')

            if not os.path.isdir(target):
                os.mkdir(target)

            for file in request.files.getlist("file"):
                print(file)
                filename = file.filename
                destination = target + filename
                print(destination)
                file.save(destination)
                return recognize(filename, target, fb_token)

def recognize(name, path, fb_token):
    # Identifies the file and file path
    FILE_NAME = name
    FOLDER_PATH = path

    # Assigns the Facebook token and sets up the graph API
    token = fb_token
    graph = facebook.GraphAPI(token)

    # # Loads the image into the memory
    # with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
    #     content = image_file.read()
    
    # image = types.Image(content=content)

    # # Performs text detection on the image file
    # responseText = client.text_detection(image=image)

    # image_text = ""

    # texts = responseText.text_annotations
    # print('Text:')

    # for i in range(len(texts)):
    #     if (i != 0):
    #         image_text += texts[i].description
    #         image_text += " "

    # print(image_text)

    # # Dataset loading
    # if not os.path.isdir('./flaskbackend/.data'):
    #     os.mkdir('./flaskbackend/.data')
    # train_dataset, test_dataset = text_classification.DATASETS['DBpedia'](
    #     root='./flaskbackend/.data', ngrams=NGRAMS, vocab=None)
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # # Model creation with dataset
    # VOCAB_SIZE = len(train_dataset.get_vocab())
    # EMBED_DIM = 32
    # NUN_CLASS = len(train_dataset.get_labels())
    # model2 = TextSentiment(VOCAB_SIZE, EMBED_DIM, NUN_CLASS).to(device)

    # # Loading state_dict from model 1 to access pretrained information
    # model2.load_state_dict(torch.load('flaskbackend/model_save.pt'))
    # model2.eval()

    # vocab = train_dataset.get_vocab()
    # model2 = model2.to("cpu")
    
    # image_category = "%s" %ag_news_label[predict(image_text, model2, vocab, 2)]

    # Now the facebook stuff starts
    findgroup(graph)
    findpost(graph)
    i = 0

    for name in names:
        print(name)

    # matching_groups = find_match(image_category, model2, vocab)
    
    # answer = "The image is classified by vision as "
    # answer += image_category
    # answer += " and the matching groups are "

    # if(len(matching_groups) >= 1):
    #     for i in range(len(matching_groups)):
    #         profile = graph.get_object(matching_groups[i], fields = 'name, email, description')
    #         print(profile["name"])
    #         answer += profile["name"]
    #         answer += " "
    #         graph.put_photo(image=open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb'), message='Facebook AI Hackathon Sample Post', album_path=matching_groups[i] + "/photos")

    # return answer

    return "Remember to uncomment Google Vision API processing"

if __name__ == '__main__':
    app.run(debug=True)
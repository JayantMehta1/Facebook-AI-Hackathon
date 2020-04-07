# Facebook-AI-Hackathon

An image processing artifical intelligence PyTorch project to detect relevant ads/content for relevant Facebook groups.

A request is sent to the user for these ads to be posted to maintain a spam free platform.

Implements the Google Cloud Vision API and Facebook Groups API.

Project completed. Will be updated here with deployment link soon.

Instructions to set up project locally on your computer:

1) Install and use python 3.8.2

2) The repository is designed as a virutal folder. It needs:
pip install google
pip install google-cloud-vision
pip install flask
pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html

3) ServiceAccountToken.json file in flaskbackend for thr Google Cloud Vision API (please use your credentials)

4) Run "npm install" under the reactfrontend directory

5) Run the "NeuralNetworkModel.py" file just once (downloads dataset for "dbpedia" and saves the trained machine learning model as "model_save.pt" for effecient use in "SentimentallyPostify.py")

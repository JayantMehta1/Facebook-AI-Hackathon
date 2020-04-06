# Facebook-AI-Hackathon

An image processing artifical intelligence PyTorch project to detect relevant ads for appropriate Facebook groups.
A request is sent to group admins for these ads to be posted to maintain a spam free platform.

Implements the Google Cloud Vision API and Facebook Groups API.

Currently under development. Will be updated by the end of the hackathon in March 2020.

Instructions to set up project:

1) Install and use python 3.8.2

2) The repository is designed as a virutal folder. It needs:
pip install google
pip install google-cloud-vision
pip install flask
pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html

3) ServiceAccountToke.JSON file in flaskbackend for thr Google Cloud Vision API (please use your credentials)

4) Run "npm install" under the reactfrontend directory

5) Run the "NeuralNetworkModel.py" file just once (downloads dataset and saves the trained machine learning model for effecient use in "SentimentallyPostify.py")

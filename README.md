# Facebook-AI-Hackathon

An image processing artifical intelligence PyTorch project to detect relevant ads/content for relevant Facebook groups.

A request is sent to the user for these ads to be posted to maintain a spam free platform.

Implements the Google Cloud Vision API and Facebook Groups API.

Here is a walkthrough for the application.

# Facebook Log In
![Login](./screenshots/LoginPage.PNG?raw=true "Login")

![Logged In](./screenshots/LoggedIn.PNG?raw=true "Logged In")

The user is able to log into their Facebook account using their credentials.

# Google Vision API Analyzes Image
![Google Vision Upload Image](./screenshots/GoogleVision.PNG?raw=true "Google Vision Upload Image")

The user can upload an image or ad of their choice to the web app. The Google Vision API is called upon and the text from the image/ad is extracted. The machine learning model runs an inference from the frozen model to predict which type of ad/image this is.

# Machine Learning Model Predicts and Matches
Analyzing the user's Facebook Groups, the machine learning model runs a prediction on each group the user has access to and matches relevant groups to the type of ad or image uploaded by the user.


# User Selects Groups from Relevant Groups
![Select Groups](./screenshots/SelectGroups.PNG?raw=true "Select Groups")

The user has a manual control of taking over the AI and confirming which groups they would like to post to. This is to protect their privacy and give them that user power of utilizing this web app service to their requirements and needs. The user can select which groups to post to and submit that back to the app.

# The Ad/Image is Posted to the Facebook Group
![Posted](./screenshots/Posted.PNG?raw=true "Posted")

The image/ad is automatically posted to the selected groups by the user from the previous steps. The user is able to effeciently share resources and content with their groups to reach large audiences for their relevant purpose.

# More Notes
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

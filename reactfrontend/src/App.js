import React from 'react';
import logo from './logo.svg';
import './App.css';

import Facebook from './components/Facebook.js'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Facebook Artificial Intelligence Hackathon: Sentimentally Postify
        </p>
        <p>My Token = {window.token}</p>
        <Facebook />
      </header>

      <main role="main" class="container">
        <div class="row">
            <div class="col-md-8">
                <form id="upload-form" method="POST" enctype="multipart/form-data">
                    <h1>Facebook Hackathon: Sentimentally Postify</h1>
                    <p>
                      Please submit an image to get a list of your Facebook groups that this image would be relevant to.
                      You will have the choice to select the groups you would like to post. Approximte time is 3 minutes.
                    </p>
                    <div class="form-group">
                        <input type="text" name="Title" placeholder="Enter a title" />
                    </div>
                    <div class="form-group" >
                        <input type="file" name="file" accept="image/*" multiple />
                    </div>
                    <input type="submit" value="Submit" />
                    <div>
                      <h2>Thank you for using Sentimentally Postify!</h2>
                    </div>
                </form>
            </div>
        </div>
    </main>

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
    </div>
  );
}


export default App;
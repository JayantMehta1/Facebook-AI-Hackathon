// import React from 'react';
// import logo from './logo.svg';
// import './App.css';

// import Facebook from './components/Facebook.js'

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Facebook Artificial Intelligence Hackathon: Sentimentally Postify
//         </p>
//         <p>My Token = {window.token}</p>
//         <Facebook />
//       </header>

//       <main role="main" class="container">
//         <div class="row">
//             <div class="col-md-8">
//                 <form id="upload-form" method="POST" enctype="multipart/form-data">
//                     <h1>Facebook Hackathon: Sentimentally Postify</h1>
//                     <p>
//                       Please submit an image to get a list of your Facebook groups that this image would be relevant to.
//                       You will have the choice to select the groups you would like to post. Approximte time is 3 minutes.
//                     </p>
//                     <div class="form-group">
//                         <input type="text" name="Title" placeholder="Enter a title" />
//                     </div>
//                     <div class="form-group" >
//                         <input type="file" name="file" accept="image/*" multiple />
//                     </div>
//                     <input type="submit" value="Submit" />
//                     <div>
//                       <h2>Thank you for using Sentimentally Postify!</h2>
//                     </div>
//                 </form>
//             </div>
//         </div>
//     </main>

//     <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
//     <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
//     <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
//     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
//     </div>
//   );
// }


// export default App;




import React, { Component } from 'react'; 

import logo from './logo.svg';
import './App.css';
import Checkbox from './Checkbox.js';
import Facebook from './components/Facebook.js';

const checkboxList = ["One", "Two", "Three", "Four", "Five"];
let checkboxToReturn = [];

class App extends React.Component {
    state = {
        checkboxes: checkboxList.reduce(
            (options, option) => ({
                ...options,
                [option]: false
            }),
            {}
        ),
        isActive: true
    };

    selectAllCheckboxes = isSelected => {
        Object.keys(this.state.checkboxes).forEach(checkbox => {
            this.setState(prevState => ({
                checkboxes: {
                    ...prevState.checkboxes,
                    [checkbox]: isSelected
                }
            }));
        });
    };

    selectAll = () => this.selectAllCheckboxes(true);

    deselectAll = () => this.selectAllCheckboxes(false);

    handleCheckboxChange = changeEvent => {
        const { name } = changeEvent.target;

        this.setState(prevState => ({
            checkboxes: {
                ...prevState.checkboxes,
                [name]: !prevState.checkboxes[name]
            }
        }));
    };
    createCheckbox = option => (
        <Checkbox
            label={option}
            isSelected={this.state.checkboxes[option]}
            onCheckboxChange={this.handleCheckboxChange}
            key={option}
        />

    );

    createCheckboxes = () => checkboxList.map(this.createCheckbox);


    handleFormSubmit = formSubmitEvent => {
        formSubmitEvent.preventDefault();
        Object.keys(this.state.checkboxes)
            .filter(checkbox => this.state.checkboxes[checkbox])
            .forEach(checkbox => {
                checkboxToReturn.push(checkbox);
                console.log(checkbox, "is selected.");
                console.log(checkboxToReturn);
            });
        this.setState({
            isActive: false
        })
    };  
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo" />
                    <div className="Intro">
                        <h1>
                            Facebook AI Hackathon
                        </h1>
                        <p>Have an image you want to share with your Facebook Groups? 
                            Fear no more, Sentimentally Postify will analyze your image and reccomend
                            the Facebook Groups your image would be relevent to using AI.
                            A plus point, you can even directly post from here!
                        </p>
                        <p> Questions/Comments: Please email me at </p>
                        <a
                        className="App-link"
                        href= 'mailto: jayant.mehta@uwaterloo.ca'
                        target="_blank"
                        rel="noopener noreferrer">
                        jayant.mehta@uwaterloo.ca
                        </a>
                    </div>
        
                    <Facebook />
                </header>

                <main role="main" class="container">
                    <div class="row">
                        <div class="col-md-8">
                            <form id="upload-form" method="POST" enctype="multipart/form-data">
                                <h1>Get started with attaching your image below</h1>
                                <div class="form-group">
                                    <input name="Title" />
                                </div>
                                <div class="form-group">
                                    <input name="Access Token" value="Plan is to get token here as a JSON" />
                                </div>
                                <div class="form-group" >
                                    <input type="file" name="file" accept="image/*" multiple />
                                </div>
                                <input id="submit" type="submit" value="Submit Image For Facebook Group Reccomendations" />
                            </form>
                            <div className="checkboxContainer">
                                {this.state.isActive ? (
                                    <form onSubmit={this.handleFormSubmit}>
                                        {this.createCheckboxes()}

                                        <div className="form-group mt-2">
                                            <button
                                                type="button"
                                                className="toSelectall"
                                                onClick={this.selectAll}
                                            >
                                                Select All
                                            </button>
                                            <button
                                                type="button"
                                                className="toDeselectall"
                                                onClick={this.deselectAll}
                                            >
                                                Deselect All
                                            </button>
                                            <button type="submit" className="SavetoSubmit">
                                                Save
                                            </button>
                                        </div>
                                    </form>
                                ) : null}
                                <p>You chose: {checkboxToReturn.map(chosenCheckbox => (<li key={chosenCheckbox}>{chosenCheckbox}</li>))}</p>
                            </div>
                        </div>
                    </div>
                </main>

                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
            </div>
        );
    }
}   
export default App;
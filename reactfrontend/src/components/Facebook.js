import React, { Component } from 'react';
import FacebookLogin from 'react-facebook-login';
import './facebookDisplay.css';


export default class Facebook extends Component {
    state = {
        isLoggedIn: false,
        userID: '',
        name: '',
        email: '',
        picture: '',
        access_token: ''
    };

    responseFacebook = response => {
        console.log(response);

        this.setState({
            isLoggedIn: true,
            userID: response.userID,
            name: response.name,
            email: response.email,
            picture: response.picture.data.url,
            access_token: response.accessToken
        });

        console.log("I recorded the values and the token is " + this.state.access_token);

        // POST
        fetch('/', {

            // Specify the method
            method: 'POST',

            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },

            // A JSON payload
            body: JSON.stringify({
                "facebook_access_token" : this.state.access_token
            })
        }).then(function (response) { // At this point, Flask has printed our JSON
            return response.text();
        }).then(function (text) {

            console.log('POST response: ');

            // Should be 'OK' if everything was successful
            console.log(text);
        });

    };

    componentClicked = () => console.log("clicked")
    render() {
        let fbContent;

        if(this.state.isLoggedIn) {
            fbContent= (
                <div className="mainDisplay">
                    <img className="profilePic" src={this.state.picture} alt={this.state.name} />
                    <h2> Welcome {this.state.name}</h2>
                    Email: {this.state.email}
                </div>

            );
        } else {
            fbContent = (
                <FacebookLogin
                appId="204445320862914"
                autoLoad={true}
                fields="name,email,picture"
                //scope="public_profile,user_friends,email,manage_pages,publish_pages,publish_to_groups,pages_show_list,groups_access_member_info"
                scope="public_profile,email, publish_to_groups,pages_show_list,groups_access_member_info"
                onClick={this.componentClicked}
                callback={this.responseFacebook} />
            )
        }
        return (
            <div>{fbContent}</div>
        )
    }
}
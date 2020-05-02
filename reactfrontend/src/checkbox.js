import React from "react";

const Checkbox = ({ label, isSelected, onCheckboxChange }) => (
    <div className="form-check">
        <label>
            <input
                type="checkbox"
                name={label}
                checked={isSelected}
                onChange={onCheckboxChange}
                className="form-check-input"
            />
            {label}
        </label>
    </div>
);

export default Checkbox;

//FAILED ATTEMPTED CODES
/*createCheckbox() {
    let checkboxToReturn = [];
    for (let i = 0; i < checkbox.length; i++) {
        checkboxStatus[i] = false;
        checkboxContainer[i] = (< p > Check box: <input type="checkbox" checked={this.state.isChecked} onChange={this.handleOptionChange} /> </p >);
        console.log("Check check" + i);
        checkboxToReturn.push(checkboxContainer[i]);
    }
    return checkboxToReturn;
    //return [<input type="checkbox" value="Testing" />, <input type="checkbox" value="Testing" />];
};
handleOptionChange() {
    if (checkboxStatus[index] === false) {
        checkboxStatus[index] = true;
    }
    else {
        checkboxStatus[index] = false;
    }
    console.log(checkboxStatus[index]);
    console.log("Confirm change! " + index);
};
handleFormSubmit = formSubmitEvent => {
    formSubmitEvent.preventDefault();
    let submitCheckbox = [];
    for (let i = 0; i < checkbox.length; i++) {
        if (checkboxStatus[i] === true) {
            submitCheckbox.push(checkboxContainer[i]);
        }
        console.log(checkboxStatus[i]);
    }
    console.log("Checkbox length is" + checkbox.length)
    return submitCheckbox;
};*/
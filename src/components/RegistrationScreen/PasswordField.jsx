import React, {useState} from 'react';
import {makeLengthValidator} from '../../utils/field-validators';
import NO_ERROR from '../../constants/NoError';

import FieldError from '../FieldError';
import './StrengthIndicator.css';


// Strength levels of passwords
const STRENGTHS = ['error', 'empty', 'poor', 'moderate', 'strong'];

// Gets the strength of password. Returns a string
function passwordStrength(pw) {
    const containsNumber = /[0-9]/g
    const containsUpperLower = /((?<=[a-z])\S*[A-Z])|((?<=[A-Z])\S*[a-z])/g
    const containsSpecialChar = /[^a-zA-Z0-9\s]/

    if (pw.match(/[\s]/g)) return STRENGTHS[0]

    if (pw.length === 0) return STRENGTHS[1];

    if (pw.length < 8 || !pw.match(containsUpperLower)) return STRENGTHS[2];

    if (pw.match(containsUpperLower) && (!pw.match(containsNumber))) return STRENGTHS[3] 
    if(!pw.match(containsSpecialChar)) return STRENGTHS[3];

    if ((pw.match(containsNumber).length + pw.match(containsSpecialChar).length < 3)) return STRENGTHS[4];

    return STRENGTHS[4]
}


/*
 *  Strength Indicator component
 *  Takes a string from the STRENGTHS array as a prop
*/
const StrengthIndicator = ({ strength }) => {
    return (
        <div id="strength-indicator-container" >
            <div id="password-strength-indicator" className={strength}>
                <div id="password-poor" />
                <div id="password-moderate" />
                <div id="password-strong" />
            </div>
            <p id="strength-indicator-text" className={strength}>
                {"Password Strength: " + strength.charAt(0).toUpperCase() + strength.slice(1)}
            </p>
        </div>
    );
}



/**
 * 
 * PasswordField component. 
 * Like the other RegistrationScreen components, it recieves an
 * update function as its prop to update the errors in the Registration Screen State
 */
const PasswordField = ({update}) => {
    const [error, setError] = useState({text:'',field:'password'});
    const [strength, setStrength] = useState('empty');
    const [fields, setFields] = useState(['',''])


    // Creates an onChange function for the actual password field (field -> 0)
    // and for the re-entry field (field->1)
    const handleOnChange = field => e => {
        // Sets Field/Strength state
        const fieldStrength = !field ? passwordStrength(e.target.value) : strength
        const fieldState = fields.slice();
        fieldState[field] = e.target.value;
        setFields(fieldState);
        setStrength(fieldStrength);

        // Sets error state
        if (fieldState[0] !== fieldState[1]) setError({text:'Passwords must match', field:'password'})
        else if (fieldStrength === STRENGTHS[3] ||  fieldStrength===STRENGTHS[4]) setError( NO_ERROR ) 
        else setError({text:'password too weak', field:'password'})
        // else setError(NO_ERROR)
    }


    return(
        <div className="register-password-container">
            <label htmlFor="password">Password</label>
            <input 
                type="password" 
                name="password"
                onBlur={e=> update(error)}
                onChange={handleOnChange(0)}
            />
            <label htmlFor="re-enter-password">Re-Enter Password</label>
            <input 
                type="password" 
                name="re-enter-password"
                onBlur={e=>update(error)}
                onChange={handleOnChange(1)}
            />
            <StrengthIndicator strength={strength}/>
            <FieldError show={true} error={error} />
        </div>
    )
}

export default PasswordField;
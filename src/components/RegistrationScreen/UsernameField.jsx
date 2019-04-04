import React, {useState} from 'react';
import FieldError from '../FieldError';
import NO_ERROR from '../../constants/NoError';
import {makeLengthValidator} from '../../utils/field-validators'


/**
 * UsernameField Component
 * Takes a function 'update' as its prop which is used to set
 * the forms error state
 */
const UsernameField = ({update}) => {
    const [error,setError] = useState(NO_ERROR);
    const [hasChanged,setHasChanged] = useState(false);

    // Creates validator function for the username.
    // Must be longer than 8 chars and no more than 16
    const validator = val => 
        makeLengthValidator(8, 17)(val) ? NO_ERROR : { text: 'Invalid username', field: 'username' };
    


    return (
        <div className="register-username-container">
            <label htmlFor="username">Username</label>
            <input 
                type="text" 
                name="username" 
                onChange={e => { setError(validator(e.target.value)) }} 
                onBlur={e=>{update(error);setHasChanged(true)}}  
            />
            <FieldError show={hasChanged} error={error} />
        </div>

    )
}

export default UsernameField;
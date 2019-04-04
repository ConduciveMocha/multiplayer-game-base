import React, {useState} from 'react';
import {emailValidator} from '../../utils/field-validators';

import FieldError from '../FieldError'
import NO_ERROR from '../../constants/NoError'



/**
 * Email Validator Component
 * Takes a function 'update' as its prop which is used to set
 * the forms error state
 */
const EmailField = ({update}) => {
    const [error,setError] = useState(NO_ERROR);
    const [hasChanged, setHasChanged] = useState(false);
    const handleChange = e => {
        setError(emailValidator(e.target.value) ? NO_ERROR : {text:'Invalid Email', field:'email'})
    }   
    
    return (
        <div className="register-email-field">
            <label htmlFor='email'>Email Address:</label>
            <input
                type="text"
                name="email"
                placeholder="example@email.com"
                onChange={handleChange}
                onBlur={e=> {update(error);setHasChanged(true)}}
            />
            <FieldError show={hasChanged} error={error} />
        </div>
    )
}
export default EmailField;
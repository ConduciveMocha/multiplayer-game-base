import React, {useState} from 'react';

// Custom hook for validating an input field
// Validator should return a list of errors
const useValidator = ( initialState,validator, preventUpdate=false) => {
    const [fieldValue, setFieldValue] = useState(initialState);
    const [fieldErrors,setFieldErrors] = useState(validator(initialState));
    const [isValid, setIsValid] = useState(fieldErrors ? true : false); // Can be used to disable button
    
    // Will be called onChange
    const fieldChange = (newValue) => {
        const errors = validator(newValue)
        
        // If preventUpdate is set, state is updated only if there are no errors
        if ((preventUpdate && !errors) || (!preventUpdate)) {
            setFieldValue(newValue);
            setFieldErrors(errors);
            setIsValid(fieldErrors ? true : false);        
        }
    }

    return {
        fieldValue,
        fieldErrors,
        isValid,
        fieldChange
    };
}

export default useValidator;
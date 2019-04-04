import React from 'react';
import PropTypes from 'prop-types'

import './field-error.css'

const FieldError = ({error,show}) => {
    
    return (

        <div className="field-error-container">
            <p className="field-error">{show ? error.text : ''}</p>
        </div>
    )
};
FieldError.propTypes = {
    error: PropTypes.shape({
        text: PropTypes.string.isRequired,
        field: PropTypes.string.isRequired
    }),
    show: PropTypes.bool.isRequired
}
export default FieldError;
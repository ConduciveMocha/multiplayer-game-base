import React, {useState, useEffect,useReducer} from 'react';
import {Link} from 'react-router-dom'
import {flaskServer} from '../../api/urls'

import NO_ERROR from '../../constants/NoError'
import FieldError from '../FieldError'


import UsernameField from './UsernameField';
import EmailField from './EmailField';
import PasswordField from './PasswordField';
import DOBField from './DOBField'

import './Registration.css'

const RegistrationScreen = (props) => {

    const [errors, setErrors] = useState({
        username: { text: '', field: 'username' },
        password: { text: '', field: 'password' },
        email: { text: '', field: 'email' },
        dob: {text:'',field:'dob'}
    });
    const [noErrors, setNoErrors] = useState(false) ;
    const hasNoErrors = obj => Object.values(obj).every(x=>x===NO_ERROR);
    

    const errorUpdate = fieldname => error => {
        const newErrors = {...errors, [fieldname]:error};
        setErrors(newErrors);
        setNoErrors(hasNoErrors(newErrors));
    }
    console.log(errors)

    return (
        <div className='registration-form-container'>

            <form 
                method="post" 
                action={flaskServer + "/register/create"}
                target="_blank"
            >
                <div className="fake-id-photo"></div>

                <UsernameField update={errorUpdate('username')}/>
                <PasswordField update={errorUpdate('password')} />
                <EmailField update={errorUpdate('email')}/>
                <DOBField update={errorUpdate('dob')}/>

                <Link to='/'>
                    <button>Back</button>
                </Link>

                <button type="submit" disabled={!noErrors}>Submit</button>

            </form>
        </div>
    )
}

export default RegistrationScreen;
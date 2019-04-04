import React, {useState,useEffect} from 'react'
import FieldError from '../FieldError'
import NO_ERROR from '../../constants/NoError'
import {makeRegexValidator} from '../../utils/field-validators';
import { getPortPromise } from 'portfinder';

const makeNumberValidator = len => makeRegexValidator(`^[0-9]{0,${len}}$`);



const DOBField = (props) =>{
    const [dobState,setDOBState] = useState({day:'',month:'',year:''})
    const [errors,setErrors] = useState({
        day:{text:'',field:'day'}, 
        month:{text:'',field:'month'}, 
        year:{text:'',field:'year'}, 
        ageError:NO_ERROR
    });

    const [showAgeError,setShowAgeError] = useState(false)
    useEffect(()=>{
        if (errors.ageError !== NO_ERROR) props.update(errors.ageError);
        else if (errors.day !== NO_ERROR) props.update(errors.day);
        else if (errors.month !== NO_ERROR) props.update(errors.month);
        else if (errors.year !== NO_ERROR) props.update(errors.year);
        else props.update(NO_ERROR);
    },[errors])


    // Checks if 18 years old
    const checkAgeValid = () => {
        const now = new Date(Date.now())
        const [curYear, curMonth, curDay] = now.toJSON().slice(0, 10).split('-')
        
        if (curYear - dobState.year < 18) return false;
        else if (curYear - dobState.year > 18) return true;
        else {
            if (dobState.month > curMonth) return true;
            else if (curMonth > dobState.month) return false;
            else {
                if (dobState.day > curDay) return true;
                else if (curDay > dobState.day) return false;
                else return true;
            }
        }
    }
    // onChange
    //
    const handleDayChange = e => {
        if (makeNumberValidator(2)(e.target.value)) setDOBState({ ...dobState, day: e.target.value});
    }
    const handleMonthChange = e => {
        if (makeNumberValidator(2)(e.target.value)) setDOBState({ ...dobState, month: e.target.value });
    }
    const handleYearChange = e => {
        if (makeNumberValidator(4)(e.target.value)) setDOBState({ ...dobState, year: e.target.value});
    }
    
    // Handler that recieves all bubbled up onChange actions
    const handleDOBChange  = e => {
        if (errors.month !== NO_ERROR || errors.day !== NO_ERROR || errors.year !== NO_ERROR) return;
        const ageError = checkAgeValid(dobState) ? NO_ERROR : { text: 'not old enough', field: 'dob' }
        setErrors({...errors, ageError:ageError });
    }

    //onBlur
    //
    // Handles focus leaving day field
    const hanldeDayBlur = e => {
        // If empty, set error and return
        if (e.target.value.length === 0) {
            setErrors({ ...errors, day: { text: 'not filled', field: 'day' } });
            return;
        }

        const day = parseInt(e.target.value);
        // If not possible day of month, setError and return
        if (day < 1 || 31 < day)  {
            setErrors({ ...errors, day: { text: 'Not Real Day', field: 'day' } });
            return;
        } 
        // Everything is hunky-dory...
        // Pad single numbers with a 0
        else if (day < 10) setDOBState({...dobState, day:"0" + day }); 
        setErrors({...errors,day:NO_ERROR});
        
    }

    // Handles focus leaving month field
    const handleMonthBlur = e => {
        // Sets error if empty
        if (e.target.value.length === 0) {
            setErrors({ ...errors, month: { text: 'not filled', field: 'month' } });
            return;
        }

        const mo = parseInt(e.target.value)
        // Invalid Month
        if (mo < 1 || 12 < mo) {
            setErrors({ ...errors, mo: { text: 'Not Real Month', field: 'month' } });
            return
        }
        //Everythings good
        // Pads single characters
        else if (mo < 10) setDOBState({...dobState,month:"0"+mo});
        setErrors({...errors,month:NO_ERROR})
    }

    // Handles focus leaving year field
    const handleYearBlur = e => {
        let fixedYear = e.target.value
        // If empty, setError & return
        if (e.target.value.length === 0) {
            setErrors({...errors,year:{text:'not filled', field:'year'}});
            return;
        }
        // Pads inputs of 1 or two characters
        else if (e.target.value.length <= 2) {
            fixedYear = e.target.value.length === 2 ? fixedYear : "0" + fixedYear // Turns single -> double
            // Sets prefix to either 19 or 20 base on a sophisticated age algorithm
            if(parseInt(fixedYear) < new Date().getYear() - 100) fixedYear = "20" + fixedYear;
            else fixedYear = "19" + fixedYear;
        }
        setDOBState({...dobState,year:fixedYear})


        const yr = parseInt(fixedYear)
        // Cant set date to future or before 1900. Returns
        if (yr < 1900 || new Date().getFullYear() < yr ) {
            console.log(yr)
            console.log(new Date().getFullYear() )
            setErrors({...errors,year:{text:'Not valid year', field:'year'}})
            return;    
        };
        // Everythings good
        setErrors({...errors, year:NO_ERROR});
    }



    return(
        <div 
            className="register-dob-container" 
            onChange={handleDOBChange}
        >
            <div className={errors.month === NO_ERROR ? 'dob-field' : 'dob-field-error'}>
                <input 
                    name="month-field"
                    className="month-field" 
                    type='text'
                    value={dobState.month}
                    onChange={handleMonthChange}
                    onBlur={handleMonthBlur}
                />
                <label htmlFor="month-field">Month</label>
            </div>
            <div className= {errors.day === NO_ERROR ? 'dob-field' : 'dob-field-error'}>
                <input 
                    name="day-field"
                    className="day-field" 
                    type='text'
                    value={dobState.day}
                    onChange={handleDayChange}
                    onBlur={hanldeDayBlur}
                />
                <label htmlFor="day-field">Day</label>
            </div>
            <div className={errors.year === NO_ERROR ? 'dob-field' : 'dob-field-error'}>
                <input 
                    name="year-field"
                    className="year-field" 
                    type='text'
                    value={dobState.year}
                    onChange={handleYearChange}
                    onBlur={handleYearBlur}
                />
                <label htmlFor="year-field">Year</label>
            </div>    
            <FieldError error={errors.ageError} show={true} />
        </div>


    )
}

export default DOBField;
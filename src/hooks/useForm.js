import React, {useState} from'react';
import useCache from './useCache';
const useform = (sendForm, formIds) => {
    const cache = useCache(formIds.map(el=>[el,null]));
    const updateForm = elName => val => {cache.set(elName,val)}
    const onSubmit = e=>{
        if(e) e.preventDefault();
        sendForm(cache.clone());
    }
    
    return {updateForm, onSubmit};
}

export default useform;



export function makeLengthValidator(minLen, maxLen = -1) {

    if (maxLen < 0) {
        if (minLen < 0) throw Error("minLen must be positive");
        else return function (input) {
            return minLen <= input.length
        };
    }
    else {
        if (maxLen <= minLen) throw Error("Argument minLen is greater than argument maxLen")
        else return function (input) {
            return minLen <= input.length && input.length <= maxLen
        };
    }
}

export const makeRegexValidator = regex =>{
    const reg =  regex instanceof RegExp ? regex : new RegExp(regex); 
    return function (s) {
        return s.match(reg)
    }
}

export function formStateValidator(formState) {
    return formState.includes('')
}


const EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
export const  emailValidator = makeRegexValidator(EMAIL_REGEX)
import React, {useState} from 'react';

// Taken from the internet, more or less...

// Custom hook for using a map
const useCache = (initialState={}) => {
    const [cache, setCache] = useState(new Map(initialState.entries()));
    
    const set = (key,value) => {setCache(new Map([...cache, [key,value]]));}
    const get = (key) => cache.get(key);
    const clear = () => {setCache(new Map())};
    const keys = () => cache.keys();
    const values = () => cache.values();
    const entries = () =>  cache.entries();
    
    // Returns a copy of cache with fn applied to the values
    const apply = (fn) => {
        let newMap = new Map();
        cache.forEach((value,key,map)=>{
            newMap.set(key,fn(value,key,map))
        });
        return newMap;
    }

    // Returns true if fn(value,key,map) evaluates to true for
    // all cache entries
    const all = (fn) => {
        let allTrue = true;
        cache.forEach((value,key,map) => {
            if (!fn(value,key,map)) allTrue = false;
        });
        return allTrue;
    }

    // Returns true if fn(value,key,map) is true for at least
    // one element in cache
    const one = (fn) => {
        let hasOne = false;
        cache.forEach((value,key,map) =>{
            if (fn(value,key,map)) hasOne = true;
        });
        return hasOne;
    }
    const clone = () => new Map(cache)
    
    return {
        get,
        set,
        clear,
        keys,
        values,
        entries,
        apply,
        all,
        one,
        clone
    };
}

export default useCache;

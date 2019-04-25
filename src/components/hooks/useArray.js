import React, { useState, useCallback } from "react";

const useArray = initial => {
  const [arr, setArr] = useState(initial);

  // Clears the array
  const clear = () => {
    setArr([]);
  };

  // Sets index to value
  const setIndex = useCallback((ind, v) => {
    setArr(arr => arr.splice(ind, 1, v));
  });
  // Removes element at index
  const removeIndex = useCallback(ind => {
    setArr(arr => arr.splice(ind, 1));
  });

  // Pushes element to end of array
  const push = v => {
    setArr(arr => [...arr, v]);
  };
  // Removes and returns last element
  const pop = () => {
    let newArr = arr.slice();
    const popped = newArr.pop();
    setArr(newArr);
    return popped;
  };
  // Sets the state to arr.map(fn)
  const map = useCallback(fn => {
    setArr(arr => arr.map(fn));
  });

  // Sets state to arr.filter(fn)
  const filter = fn => arr.filter(fn);

  return {
    arr,
    setArr,
    clear,
    setIndex,
    removeIndex,
    push,
    pop,
    map,
    filter
  };
};
export default useArray;

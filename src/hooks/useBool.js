import { useState, useCallback } from "react";

const useBool = init => {
  const [value, setValue] = useState(init);
  return {
    value,
    setValue,
    toggle: useCallback(() => setValue(value => !value), []),
    setTrue: useCallback(() => setValue(true), []),
    setFalse: useCallback(() => setValue(false), [])
  };
};

export default useBool;

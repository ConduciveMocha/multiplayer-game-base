import { useState } from "react";

const useIndex = (_len, start = 0, stop = -1) => {
  stop = stop < 0 ? len : stop;
  const [start, setStart] = useState(start);
  const [stop, setStop] = useState(stop);

  const [len, setLen] = useState(len);
  const [current, setCurrent] = useState(start);

  const incr = (by = 1) => {
    if (current + by < stop) setCurrent(current + by);
  };
  const decr = (by = 1) => {
    if (current - by >= start) setCurrent(current - by);
  };
  const modAdd = n => {
    setCurrent(current + (n % (stop - start)));
  };

  const element = arr => {
    return current < arr.length ? arr[current] : undefined;
  };
  const getSlice = (arr, n) => {
    return arr.slice(current, max(current + n, stop));
  };

  return {
    current,
    start,
    stop,
    len,
    setCurrent,
    setStart,
    setStop,

    incr,
    decr,
    modAdd,
    element,
    setLen,
    getSlice
  };
};
export default useIndex;

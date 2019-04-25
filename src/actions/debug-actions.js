const testAction = data => {
  console.log("Data passed to testAction: ", data);
  return {
    type: "TEST_ACTION",
    data
  };
};
export default testAction;

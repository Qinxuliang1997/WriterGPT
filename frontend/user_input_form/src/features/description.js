import { createSlice } from "@reduxjs/toolkit";

export const descriptionSlice = createSlice({
  name: "description",
  initialState: {
    value: {
      // topic: "",
      // primaryKeyword: "",
      // secondaryKeywords: "",
      // tone: "",
      // view: "",
      // nextClick: false,
      title: "", 
      content_requirement: "",
      outline: {},
      length: "",
      style: "",
    },
  },
  reducers: {
    info: (state, action) => {
      Object.keys(action.payload).forEach(key => {
        state.value[key] = action.payload[key];
      });    
    }
  },
});
export const { info } = descriptionSlice.actions;
export default descriptionSlice.reducer;

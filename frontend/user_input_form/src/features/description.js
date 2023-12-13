import { createSlice } from "@reduxjs/toolkit";

export const articleSlice = createSlice({
  name: "article",
  initialState: {
    value: {
      topic: "",
      primaryKeyword: "",
      secondaryKeywords: "",
      tone: "",
      view: "",
      nextClick: false,
      title: "", 
      outline: "",
    },
  },
  reducers: {
    info: (state, action) => {
      state.value = action.payload;
    }
  },
});
export const { info } = articleSlice.actions;
export default articleSlice.reducer;

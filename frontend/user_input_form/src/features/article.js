import { createSlice } from "@reduxjs/toolkit";

export const articleSlice = createSlice({
  name: "article",
  initialState: {
    value: {
        title: "",
        content: {},
    },
  },
  reducers: {
    fill: (state, action) => {
      Object.keys(action.payload).forEach(key => {
        state.value[key] = action.payload[key];
      });    
    },
    updateContent: (state, action) => {
      state.value.content = action.payload;
    }
  },
});
export const { fill,updateContent } = articleSlice.actions;
export default articleSlice.reducer;

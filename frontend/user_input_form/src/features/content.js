import { createSlice } from "@reduxjs/toolkit";

export const contentSlice = createSlice({
  name: "content",
  initialState: {
    value: {
        content: "",
    },
  },
  reducers: {
    fill: (state, action) => {
      state.value = action.payload;
    }
  },
});
export const { fill } = contentSlice.actions;
export default contentSlice.reducer;

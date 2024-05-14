import { createSlice } from "@reduxjs/toolkit";

export const descriptionSlice = createSlice({
  name: "description",
  initialState: {
    value: {
      topic: "",
      primaryKeyword: "",
      // secondaryKeywords: "",
      // tone: "",
      // view: "",
      nextClick: false,
      title: "", 
      outline: {
        '小节 1': {
            'title': "小节标题1",
            'paragraphs': {
                '段落 1': {'content': "这是第一段内容。"},
                '段落 2': {'content': "这是第二段内容。"}
            }
        },
        '小节 2': {
            'title': "小节标题2",
            'paragraphs': {
                '段落 1': {'content': "小节2的第一段内容。"}
            }
        }
      },
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

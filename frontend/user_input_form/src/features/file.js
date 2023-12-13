// fileUploadSlice.js
import { createSlice } from '@reduxjs/toolkit';

export const fileUploadSlice = createSlice({
  name: 'fileUpload',
  initialState: {
    files: [], //  An array of files that are being uploaded. 
    uploadProgress: {}, // An object that maps file names to upload progress. 
    uploadStatus: 'idle', // The current upload status, can be 'idle', 'uploading', 'success', 'failure'
    errorMessage: '' //  An error message that is displayed if the upload fails. 
  },
  reducers: {
    addFile: (state, action) => {
      state.files.push(action.payload);
    },
    setUploadProgress: (state, action) => {
      const { fileName, progress } = action.payload;
      state.uploadProgress[fileName] = progress;
    },
    setUploadStatus: (state, action) => {
      state.uploadStatus = action.payload;
    },
    setErrorMessage: (state, action) => {
      state.errorMessage = action.payload;
    },
    resetUpload: (state) => {
      state.files = [];
      state.uploadProgress = {};
      state.uploadStatus = 'idle';
      state.errorMessage = '';
    }
  },
});

export const { addFile, setUploadProgress, setUploadStatus, setErrorMessage, resetUpload } = fileUploadSlice.actions;

export default fileUploadSlice.reducer;

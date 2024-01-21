import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/style.css';
import 'quill/dist/quill.snow.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {configureStore} from '@reduxjs/toolkit'
import { Provider } from 'react-redux';
import pageReducer  from './features/pages';
import articleReducer from './features/description'
import fileUploadReducer from './features/file';
import contentReducer from './features/content'

const store=configureStore({
  reducer: {
    page: pageReducer,
    article: articleReducer,
    fileUpload: fileUploadReducer,
    content: contentReducer,
  },
})

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

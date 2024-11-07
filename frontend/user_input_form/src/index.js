import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/style.css';
import 'quill/dist/quill.snow.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'normalize.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {configureStore} from '@reduxjs/toolkit'
import { Provider } from 'react-redux';
import pageReducer  from './features/pages';
import descriptionReducer from './features/description'
import fileUploadReducer from './features/file';
import articleReducer from './features/article'
import './interceptors/axios';

const store=configureStore({
  reducer: {
    page: pageReducer,
    description: descriptionReducer,
    fileUpload: fileUploadReducer,
    article: articleReducer,
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

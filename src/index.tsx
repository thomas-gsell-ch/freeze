import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
//import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import { BrowserRouter, Routes, Route } from "react-router"
import Add from './Add/Add'
import Detail from './Detail/Detail'
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/add" element={<Add />} />
      <Route path="/detail" element={<Detail />} />
    </Routes>
  </BrowserRouter>
);

reportWebVitals();
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
//serviceWorkerRegistration.unregister();

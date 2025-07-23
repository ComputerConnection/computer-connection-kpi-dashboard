import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sales from './pages/Sales';
import Quotes from './pages/Quotes';
import Repairs from './pages/Repairs';
import Personal from './pages/Personal';
import Layout from './pages/Layout';

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}> 
          <Route path="/" element={<Sales />} />
          <Route path="/sales" element={<Sales />} />
          <Route path="/quotes" element={<Quotes />} />
          <Route path="/repairs" element={<Repairs />} />
          <Route path="/personal" element={<Personal />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Components
import LoginForm from "./pages/LoginForm";
import Home from './pages/Home';
import AdminHome from "./pages/admin/AdminHome";
import ManagementDataSet from "./pages/admin/ManagementDataSet";
import ManagementMedical from "./pages/admin/ManagementMedical";
import ManagementHospital from "./pages/admin/ManagementHospital";
import Diagnostic from "./pages/diagnostic/Diagnostic";
import History from "./pages/diagnostic/History";
import Logout from "./pages/Logout";

// Css
import "./App.css";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* Ruta para el formulario de login */}
          <Route path="/login" element={<LoginForm />} />
          <Route path="/logout" element={<Logout/>} />
          <Route path="/adminhome" element={<AdminHome />} />
          <Route path="/dataset" element={<ManagementDataSet/>} />
          <Route path="/medical" element={<ManagementMedical/>} />
          <Route path="/hospital" element={<ManagementHospital/>} />
          <Route path="/diagnostic" element={<Diagnostic/>} />
          <Route path="/history" element={<History/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

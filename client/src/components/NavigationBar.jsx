import React, { useEffect, useState } from 'react';
import { Outlet, Link, useNavigate } from "react-router-dom";
import { FaUserMd, FaHospital, FaHistory, FaHome, FaImages, FaList, FaLock, FaUnlock, FaUniversity } from 'react-icons/fa';

import logo from '../assets/logo_1.png';
import '../styles/NavigationBar.css';

function NavigationBar() {
    const [isAuth, setIsAuth] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
            setIsAuth(true);
            const adminValue = localStorage.getItem('admin') === "true";
            setIsAdmin(adminValue);
        }
    }, []);

    // Nueva función para manejar el click en el logo
    const handleLogoClick = (e) => {
        e.preventDefault();
        if (!isAuth) {
            navigate("/");
        } else if (isAuth && isAdmin) {
            navigate("/adminhome");
        } else if (isAuth && !isAdmin) {
            navigate("/admindiagnostic");
        }
    };

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div className="container">
                    {/* Logo con navegación condicional */}
                    <a
                        className="navbar-brand d-flex align-items-center"
                        href="#"
                        onClick={handleLogoClick}
                        style={{ cursor: "pointer" }}
                    >
                        <img src={logo} alt="Instrumental médico" />
                    </a>

                    {/* Botón de colapso para dispositivos móviles */}
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarNav"
                        aria-controls="navbarNav"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    {/* Opciones de menú */}
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto">
                            {/* Menu general */}
                            {!isAuth && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/"><FaHome /> Inicio</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/about"><FaUniversity /> Acerca De</Link>
                                    </li>
                                </>
                            )}
                            {/* Menu del doctor */}
                            {isAuth && !isAdmin && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/admindiagnostic"><FaHome /> Inicio</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/diagnostic"><FaList /> Evaluar</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/history"><FaHistory /> Historial</Link>
                                    </li>
                                </>
                            )}
                            {/* Menu del Admin */}
                            {isAuth && isAdmin && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/adminhome"><FaHome /> Inicio</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/dataset"><FaImages /> DataSet</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/medical"><FaUserMd /> Médicos</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/hospital"><FaHospital /> Hospitales</Link>
                                    </li>
                                </>
                            )}
                        </ul>
                        {/* Botón de login */}
                        <Link className="btn btn-light d-flex align-items-center ms-3" to={isAuth ? "/logout" : "/login"}>
                            <i className="bi bi-person-circle text-purple me-2" style={{ fontSize: "1.5rem", marginRight: "0.5rem" }}></i>
                            {isAuth ? (
                                <>
                                    <FaLock style={{ marginRight: "0.5rem" }} /> Salir
                                </>
                            ) : (
                                <>
                                    <FaUnlock style={{ marginRight: "0.5rem" }} /> Iniciar
                                </>
                            )}
                        </Link>
                    </div>
                </div>
            </nav>
            <Outlet />
        </>
    );
}

export default NavigationBar;

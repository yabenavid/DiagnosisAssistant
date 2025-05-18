import React, { useEffect, useState } from 'react';
import { Outlet, Link } from "react-router-dom";
import { FaUserMd, FaHospital, FaHistory, FaHome, FaImages, FaList, FaLock, FaUnlock } from 'react-icons/fa';

import logo from '../assets/logo.png';
import '../styles/NavigationBar.css';

function NavigationBar() {
    const [isAuth, setIsAuth] = useState(false);
    const [isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
            console.log("Si hay token de acceso");
            setIsAuth(true);

            // Convierte el valor de localStorage a booleano
            const adminValue = localStorage.getItem('admin') === "true";
            setIsAdmin(adminValue);
            console.log("Es admin: ", adminValue);
        }
    }, []);

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div className="container">
                    {/* Logo */}
                    <a className="navbar-brand d-flex align-items-center" href="#">
                        <i className="bi bi-activity text-purple" style={{ fontSize: "1.5rem", marginRight: "0.5rem" }}></i>
                        <span className="fw-bold text-white">Asistente </span>
                        <span className="fw-bold text-success"> OncoJuntas</span>
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
                                        <Link className="nav-link" to="/about">Acerca De</Link>
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

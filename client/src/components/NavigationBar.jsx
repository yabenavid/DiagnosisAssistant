import React from 'react';
import { useEffect, useState } from "react";
import { Outlet, Link } from "react-router-dom";
import '../styles/NavigationBar.css';

function NavigationBar() {
    const [isAuth, setIsAuth] = useState(false);

    const [ isAdmin, setIsAdmin] = useState(false);

    useEffect(() => {
        if (localStorage.getItem('access_token') !== null) {
            setIsAuth(true);
            setIsAdmin(localStorage.getItem('admin'));
        }
    }, [isAuth], [isAdmin]);
    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div className="container">
                    {/* Logo */}
                    <a className="navbar-brand d-flex align-items-center" href="#">
                        <i className="bi bi-activity text-purple" style={{ fontSize: "1.5rem", marginRight: "0.5rem" }}></i>
                        <span className="fw-bold text-white">Asistente </span>
                        <span className="fw-bold text-success">OncoJuntas</span>
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
                                        <Link className="nav-link" to="/">INICIO</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/about">ACERCA DE</Link>
                                    </li>
                                </>
                            )}
                            {/* Menu del doctor */}
                            {isAuth && !isAdmin && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/diagnostic">EVALUAR</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/history">HISTORIAL</Link>
                                    </li>
                                </>
                            )}
                            {/* Menu del Admin */}
                            {isAuth && isAdmin && (
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/adminhome">INICIO</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/dataset">GESTIÓN DATASET</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/medical">GESTIÓN MEDICOS</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/hospital">GESTIÓN HOSPITAL</Link>
                                    </li>
                                </>
                            )}
                        </ul>
                        {/* Botón de login */}
                        <Link className="btn btn-light d-flex align-items-center ms-3" to={isAuth ? "/logout" : "/login"}>
                            <i className="bi bi-person-circle text-purple me-2" style={{ fontSize: "1.5rem" }}></i>
                            {isAuth ? "Salir" : "Entrar"}
                        </Link>
                    </div>
                </div>
            </nav>
            <Outlet />
        </>
    );
}

export default NavigationBar;

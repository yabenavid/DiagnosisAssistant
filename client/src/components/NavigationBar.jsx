import React from 'react';
import { Outlet, Link } from "react-router-dom";
import '../styles/NavigationBar.css';

function NavigationBar() {
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
                            <li className="nav-item">
                                <Link className="nav-link" to="/">INICIO</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/about">ACERCA DE</Link>
                            </li>
                            {/* <li className="nav-item">
                                <Link className="nav-link" to="/departments">DEPARTAMENTOS</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/info">INFORMACIÓN</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" to="/other">OTRO</Link>
                            </li> */}
                        </ul>
                        {/* Botón de login */}
                        <Link className="btn btn-light d-flex align-items-center ms-3" to="/login">
                            <i className="bi bi-person-circle text-purple me-2" style={{ fontSize: "1.5rem" }}></i>  
                            Entrar
                        </Link> 
                    </div>
                </div>
            </nav>
            <Outlet />
        </>
    );
}

export default NavigationBar;

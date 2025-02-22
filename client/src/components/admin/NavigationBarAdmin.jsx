import React, { Component } from 'react';
import { Outlet, Link } from "react-router-dom";

function NavigationBarAdmin(){
    return(
        <>
        <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
                <div className="container">
                    {/* Logo */}
                    <a className="navbar-brand d-flex align-items-center" href="#">
                        <i className="bi bi-activity text-purple" style={{ fontSize: "1.5rem", marginRight: "0.5rem" }}></i>
                        <span className="fw-bold text-purple">Asistente</span>
                        <span className="fw-bold text-success">Juntas Oncológicas</span>
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
                                <a className="nav-link text-purple fw-bold" href="#">
                                <Link to="/adminhome">INICIO</Link>
                                </a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link text-dark fw-bold" href="#">
                                <Link to="/dataset">GESTIÓN DATASET</Link>
                                </a>
                            </li>
                            <li className="nav-item">
                                <a className="nav-link text-dark fw-bold" href="#">
                                <Link to="/medical">GESTIÓN MEDICOS</Link>
                                </a>
                            </li>

                            <li className="nav-item">
                            <a className="nav-link text-dark fw-bold" >
                                <Link to="/hospital">GESTIÓN HOSPITAL</Link>
                                </a>
                            </li>
                            
                        </ul>
                        {/* Botón de login */}
                        <a className="btn btn-light d-flex align-items-center ms-3" href="#">
                            <i className="bi bi-person-circle text-purple me-2" style={{ fontSize: "1.5rem" }}></i>  
                            <Link to="/">Salir</Link> 
                        </a>
                    </div>
                </div>
            </nav>
            <Outlet />
        </>
    )
    
}

export default NavigationBarAdmin;
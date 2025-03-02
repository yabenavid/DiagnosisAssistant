import React, { Component } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios'

// APis
import { LogoutUser } from '../api/logout.api';

export const Logout = async () => {
    const navigate = useNavigate();
    const refresh = { "refresh_token": localStorage.getItem('refresh_token') };
    try {
        // Llamada a la API
        const response = await LogoutUser(refresh);
        console.log("Respuesta del servidor Logout:", response?.status);
        localStorage.clear();
        axios.defaults.headers.common['Authorization'] = null;
        navigate("/login");

    } catch (error) {
        console.error("Error al cerrar sesión:", error);
        window.location.href = '/'
        alert("Ocurrió un error al cerrar sesión. Intente nuevamente..");
    }

    return (
        <>
            <div></div>
        </>
    )

}

export default Logout;
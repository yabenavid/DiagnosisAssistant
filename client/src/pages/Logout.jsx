import React, { useEffect, useRef } from 'react';
import { useNavigate } from "react-router-dom";
import axios from 'axios';

// APIs
import { LogoutUser } from '../api/logout.api';

const Logout = () => {
    const navigate = useNavigate();
    const hasLoggedOut = useRef(false); // Indicador para evitar múltiples llamadas

    useEffect(() => {
        const performLogout = async () => {
            if (hasLoggedOut.current) return; // Si ya se ejecutó, no hacer nada
            hasLoggedOut.current = true; // Marcar como ejecutado

            const refresh = { "refresh_token": localStorage.getItem('refresh_token') };
            try {
                // Llamada a la API
                const response = await LogoutUser(refresh);
                console.log("Respuesta del servidor Logout:", response?.status);
                localStorage.clear();
                axios.defaults.headers.common['Authorization'] = null;
                navigate("/login"); // Redirige al login
            } catch (error) {
                console.error("Error al cerrar sesión:", error);
                alert("Ocurrió un error al cerrar sesión. Intente nuevamente.");
                navigate("/"); // Redirige al inicio en caso de error
            }
        };

        performLogout();
    }, [navigate]); // Se ejecuta solo una vez al montar el componente

    return (
        <div>
            <p>Cerrando sesión...</p>
        </div>
    );
};

export default Logout;
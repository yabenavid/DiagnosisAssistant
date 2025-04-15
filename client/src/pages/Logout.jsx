import React, { useEffect, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { LogoutUser } from '../api/logout.api';

const Logout = () => {
    const { auth }      = useAuth();
    const navigate      = useNavigate();
    const hasLoggedOut  = useRef(false);

    useEffect(() => {
        const performLogout = async () => {
            if (hasLoggedOut.current) return;
            hasLoggedOut.current = true;

            const refresh = { "refresh_token": localStorage.getItem('refresh_token') };
            try {
                await LogoutUser(refresh, auth.accessToken);
                localStorage.clear();
                axios.defaults.headers.common['Authorization'] = null;
                navigate("/login");
            } catch (error) {
                console.error("Error al cerrar sesión:", error);
                localStorage.clear();
                alert("Ocurrió un error al cerrar sesión. Intente nuevamente.");
                navigate("/");
            }
        };

        performLogout();
    }, [navigate]);

    return (
        <div>
            <p>Cerrando sesión...</p>
        </div>
    );
};

export default Logout;
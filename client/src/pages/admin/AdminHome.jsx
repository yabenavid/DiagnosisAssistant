import React, { Component } from 'react';
import { NavigationBar, Footer } from '../../components';
import { useEffect} from "react";
import { useNavigate } from "react-router-dom";


import '/src/styles/admin/AdminHome.css';

function AdminHome() {
    const navigate = useNavigate();
    useEffect(() => {
        if(localStorage.getItem('access_token') === null){                   
            navigate("/login");
        }
    }, []);

    return (
        <>
            
            <div>
                <NavigationBar />
                <div className="callout-info">Bienvenido a la Gestion de Administrador</div>
                <Footer />
            </div>

        </>
    )

}

export default AdminHome;

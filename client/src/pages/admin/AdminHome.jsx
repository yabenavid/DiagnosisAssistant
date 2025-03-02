import React, { Component } from 'react';
import { NavigationBarAdmin, Footer } from '../../components';
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
                <NavigationBarAdmin></NavigationBarAdmin>
                <div class="callout-info">Bienvenido a la Gestion de Administrador</div>
                <Footer></Footer>
            </div>

        </>
    )

}

export default AdminHome;

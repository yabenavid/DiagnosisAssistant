import React, { Component } from 'react';
import { NavigationBarAdmin, Footer } from '../../components';
import '/src/styles/admin/AdminHome.css';
function AdminHome() {
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

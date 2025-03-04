import React, { Component } from 'react';
import { NavigationBar, Footer } from '../../components';
import { useEffect} from "react";
import { useNavigate } from "react-router-dom";

function History() {
    const navigate = useNavigate();
    
    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        }
    }, []);
    
    return (
        <>
            <div>
                <NavigationBar />
                <div class="callout-info">Historial de Diagnostico</div>
                <Footer></Footer>
            </div>

        </>
    )

}

export default History;
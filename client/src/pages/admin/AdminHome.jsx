import React, { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { NavigationBar, Footer } from '../../components';
import { FaUserMd, FaHospital, FaImages, FaSignOutAlt } from 'react-icons/fa';
import '/src/styles/admin/AdminHome.css';

function AdminHome() {
    const navigate = useNavigate();

    useEffect(() => {
        if (!localStorage.getItem('access_token')) {
            navigate("/login");
        }
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate("/login");
    };

    const adminCards = [
        {
            title: "DataSet",
            icon: <FaImages size={40} />,
            link: "/dataset",
            color: "#2a7e5e"
        },
        {
            title: "Hospitales",
            icon: <FaHospital size={40} />,
            link: "/hospital",
            color: "#9155a7"
        },
        {
            title: "Médicos",
            icon: <FaUserMd size={40} />,
            link: "/medical",
            color: "#2a7e5e"
        }
        
    ];

    return (
        <div className="admin-container">
            <NavigationBar />

            <div className="dashboard-container">
                <div className="welcome-banner">
                    <h2>Bienvenido al administrador de OncoJuntas</h2>
                    <p> Asistente para el apoyo a juntas médicas
                        oncológicas en el diagnóstico de cáncer de estómago a partir del uso de
                        herramientas de segmentación </p>
                </div>

                <div className="cards-grid">
                    {adminCards.map((card, index) => (
                        <div
                            key={index}
                            className="admin-card"
                            onClick={() => navigate(card.link)}
                            style={{ '--card-color': card.color }}
                        >
                            <div className="card-icon">{card.icon}</div>
                            <h3>{card.title}</h3>
                            <p>Gestionar y administrar {card.title.toLowerCase()}</p>
                        </div>
                    ))}
                </div>
            </div>

            <Footer />
        </div>
    )
}

export default AdminHome;
import React from 'react';
import '../styles/Footer.css';

function Footer() {
    return (
        <>
            <footer>
                <div className="container">
                    <div className="row">
                        {/* Logo y Descripción */}
                        <div className="col-md-4 mb-3">
                            <h5>My Website</h5>
                            <p>
                                Tu plataforma para contenido increíble y recursos útiles.
                                Inspírate y aprende con nosotros.
                            </p>
                        </div>

                        {/* Navegación */}
                        <div className="col-md-4 mb-3">
                            <h5>Enlaces útiles</h5>
                            <ul className="list-unstyled">
                                <li><a href="#">Inicio</a></li>
                                <li><a href="#">Sobre nosotros</a></li>
                                <li><a href="#">Servicios</a></li>
                                <li><a href="#">Contacto</a></li>
                            </ul>
                        </div>

                        {/* Redes Sociales */}
                        <div className="col-md-4 mb-3">
                            <h5>Síguenos</h5>
                            <div className="social-icons">
                                <a href="#"><i className="bi bi-facebook"></i></a>
                                <a href="#"><i className="bi bi-twitter"></i></a>
                                <a href="#"><i className="bi bi-instagram"></i></a>
                            </div>
                        </div>
                    </div>

                    <div className="footer-bottom text-center">
                        <p>&copy; {new Date().getFullYear()} Universidad del Cauca. Todos los derechos reservados</p>
                    </div>
                </div>
            </footer>
        </>
    );
}

export default Footer;

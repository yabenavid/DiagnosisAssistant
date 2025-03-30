import React from 'react';
import '../styles/Footer.css';
import youtubeIcon from '../assets/youtube.png';
import facebookIcon from '../assets/facebook.png';
import instagramIcon from '../assets/instagram.png';

function Footer() {
    return (
        <>
            <footer>
                <div className="container">
                    <div className="row">
                        {/* Logo y Descripción */}
                        <div className="col-md-4 mb-3">
                            <h5>Universidad del Cauca
                            NIT. 891500319-2</h5>
                            <p>
                            Posteris Lvmen Moritvrvs Edat (Quién ha de morir deje su luz a la posteridad).
                            </p>
                        </div>

                        {/* Navegación */}
                        <div className="col-md-4 mb-3">
                            <h5>Enlaces útiles</h5>
                            <ul className="list-unstyled">
                                <li><a href="https://www.unicauca.edu.co/">Unicauca</a></li>
                                <li><a href="https://www.unicauca.edu.co/atencion-al-ciudadano/">Contacto</a></li>
                                {/* <li><a href="#">Servicios</a></li>
                                <li><a href="#">Contacto</a></li> */}
                            </ul>
                        </div>

                        {/* Redes Sociales */}
                        <div className="col-md-4 mb-3">
                            <h5>Síguenos</h5>
                            <div className="social-icons">
                                <a href="https://www.youtube.com/user/unicaucapopayan"><img src={youtubeIcon} alt="YouTube" className="social-icon" /></a>
                                <a href="https://www.facebook.com/universidadelcauca/"><img src={facebookIcon} alt="Facebook" className="social-icon" /></a>
                                <a href="https://www.instagram.com/universidadelcauca/"><img src={instagramIcon} alt="Instagram" className="social-icon" /></a>
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

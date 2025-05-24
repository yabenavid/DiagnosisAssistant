import React from "react";
import { HomeCarousel, Footer, NavigationBar } from '../components';
import "/src/styles/About.css";

const AcercaDe = () => {
    return (
        <>
        <NavigationBar />
        <div className="about-container">
            <section className="about-section">
                <div className="image-container">
                    <img 
                        src="/src/assets/STR_458.png" 
                        alt="Instrumental médico" 
                    />
                </div>
                <div className="text-container">
                    <h3>Acerca de OncoJuntas</h3>
                    <p>
                        Párrafo. Haz clic para editar y agregar tu propio texto. Es fácil. 
                        Haz clic en "Editar texto" o doble clic aquí para agregar tu contenido y cambiar la fuente.
                        Puedes arrastrar y soltar este texto donde quieras en tu página. En este espacio puedes contar 
                        tu historia y permitir a los usuarios saber más sobre ti.
                    </p>
                    <p>
                        Este es un buen espacio para hablar sobre tu empresa y servicios. Usa este espacio para incluir 
                        más detalles sobre tu empresa. Escribe sobre tu equipo y los servicios que ofreces.
                    </p>
                </div>
            </section>

            <section className="members-section">
                <h2>Participantes</h2>
                <div className="members-grid">
                    <div className="member-card">
                        <img src="/ruta/a/medico1.jpg" alt="Dr. Andrés Abad" />
                        <h4>Yeferson Benavides</h4>
                        <p>
                            Párrafo. Haz clic aquí para agregar tu texto y editar. Permite que tus usuarios te conozcan.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src="/ruta/a/medico2.jpg" alt="Dra. Amelia Casas" />
                        <h4>Yennyfer Aviles</h4>
                        <p>
                            Párrafo. Haz clic aquí para agregar tu texto y editar. Permite que tus usuarios te conozcan.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src="/ruta/a/medico3.jpg" alt="Dr. Antonio Rueda" />
                        <h4>Dr. Ricardo Zambrano</h4>
                        <p>
                            Párrafo. Haz clic aquí para agregar tu texto y editar. Permite que tus usuarios te conozcan.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src="/ruta/a/medico3.jpg" alt="Dr. Antonio Rueda" />
                        <h4>Dr. Ember Martinez</h4>
                        <p>
                            Párrafo. Haz clic aquí para agregar tu texto y editar. Permite que tus usuarios te conozcan.
                        </p>
                    </div>
                </div>
            </section>
        </div>
        <Footer />
        </>
    );
};

export default AcercaDe;

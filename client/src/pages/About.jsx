import React from "react";
import { HomeCarousel, Footer, NavigationBar } from '../components';
import Segmented from '../assets/segmented_1.png';
import IngEmber from '../assets/IMG_8384.png';
import IngRicardo from '../assets/IMG_8385.jpg';
import IngYeferson from '../assets/IMG_8387.jpeg';
import IngYennyfer from '../assets/IMG_8386.jpeg';

import "/src/styles/About.css";

const AcercaDe = () => {
    return (
        <>
        <NavigationBar />
        <div className="about-container">
            <section className="about-section">
                <div className="image-container">
                    <img 
                        src={Segmented}  
                        alt="Instrumental médico" 
                    />
                </div>
                <div className="text-container">
                    <h3>Acerca de OncoJuntas</h3>
                    <p>
                        Es un modelo de asistente para el apoyo a juntas médicas oncológicas en el diagnóstico de cáncer de estómago a partir del uso de herramientas de segmentación como Segment Anything Model (SAM) y Scikit-Image.
                    </p>
                    <p>
                        El proyecto integra herramientas de segmentación y bases de datos abiertas para optimizar el diagnóstico de cáncer de estómago, potenciando la precisión en juntas médicas y el desarrollo de IA aplicada. Además, democratiza el acceso a tecnologías avanzadas, estableciendo estándares innovadores en detección temprana y tratamiento. Su impacto dual: mejorar resultados clínicos y expandir conocimiento técnico en oncología.
                    </p>
                </div>
            </section>

            <section className="members-section">
                <h2>Participantes</h2>
                <div className="members-grid">
                    <div className="member-card">
                        <img src={IngEmber} alt="Ing. Ember Martinez" />
                        <h4>Ing. Ember Martinez (Director)</h4>
                        <p>
                            Ingeniero de Sistemas de la Universidad Nacional de Colombia, Sede Bogotá, graduado en 2001. Posteriormente, obtuvo una Maestría en Ingeniería con énfasis en Ingeniería de Sistemas y Computación de la Universidad del Valle en 2011. Actualmente es un Especialista en Redes y Servicios Telemáticos de la Universidad del Cauca.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src={IngRicardo} alt="Ing. Ricardo Zambrano" />
                        <h4>Ing. Ricardo Zambrano (Coodirector)</h4>
                        <p>
                            Ingeniero de Sistemas y Computación, Universidad de los Andes. Maestría en Administración de Negocios, Universidad de Phoenix. Diplomado en Gestión y Articulación de Procesos Asociativos, Universidad Javeriana. Diplomado en Gerencia de la Tecnología y la Innovación, Universidad del Cauca. Diplomado en Alta Gerencia, Universidad ICESI.
                        </p>
                    </div>
                    
                    <div className="member-card">
                        <img src={IngYeferson} alt="Yeferson Benavides Marín" />
                        <h4>Yeferson Benavides (Estudiante)</h4>
                        <p>
                            Estudiante de Ingeniería de Sistemas de la Universidad del Cauca.
                            Actualmente colaborador en el área del Adobe Commerce (Magento) 

                        </p>
                    </div>
                    <div className="member-card">
                        <img src={IngYennyfer} alt="Yennyfer Aviles Ramírez" />
                        <h4>Yennyfer Aviles (Estudiante)</h4>
                        <p>
                            Estudiante de Ingeniería de Sistemas de la Universidad del Cauca.
                            Actualmente colaboradora en el área del Adobe Commerce (Magento)
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

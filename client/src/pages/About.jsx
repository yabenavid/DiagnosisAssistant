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
                        src="/src/assets/segmented_1.png" 
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
                        <img src="/src/assets/ember.png" alt="Ing. Ember Martinez" />
                        <h4>Ing. Ember Martinez (Director)</h4>
                        <p>
                            Ingeniero de Sistemas de la Universidad Nacional de Colombia, Sede Bogotá, graduado en 2001. Posteriormente, obtuvo una Maestría en Ingeniería con énfasis en Ingeniería de Sistemas y Computación de la Universidad del Valle en 2011. Actualmente es un Especialista en Redes y Servicios Telemáticos de la Universidad del Cauca.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src="/src/assets/ricardo.jpg" alt="Ing. Ricardo Zambrano" />
                        <h4>Ing. Ricardo Zambrano (Coodirector)</h4>
                        <p>
                            Ingeniero de Sistemas y Computación, Universidad de los Andes. Maestría en Administración de Negocios, Universidad de Phoenix. Diplomado en Gestión y Articulación de Procesos Asociativos, Universidad Javeriana. Diplomado en Gerencia de la Tecnología y la Innovación, Universidad del Cauca. Diplomado en Alta Gerencia, Universidad ICESI.
                        </p>
                    </div>
                    
                    <div className="member-card">
                        <img src="/src/assets/yefer.jpeg" alt="Yeferson Benavides" />
                        <h4>Yeferson Benavides (Estuadiante)</h4>
                        <p>
                            Estudiante de Ingeniría de Sistema de la Universidad del Cauca.
                        </p>
                    </div>
                    <div className="member-card">
                        <img src="/src/assets/yenn.jpg" alt="Yennyfer Aviles" />
                        <h4>Yennyfer Aviles (Estuadiante)</h4>
                        <p>
                            Estudiante de Ingeniría de Sistema de la Universidad del Cauca.
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

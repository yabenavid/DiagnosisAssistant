import { HomeCarousel, Footer, NavigationBar } from '../components';
import Information from './Information';
import '../styles/Home.css';

import Banner from '../assets/banner1.png'

function Home() {
    return (
        <>
            <NavigationBar />

            {/* Contenedor principal para el contenido debajo del NavigationBar */}
            <div className="main-content">
                <header>
                    <h1>Asistente para Juntas Médicas Oncológicas</h1>
                    {/* <p>Cáncer de Estómago</p> */}
                    {/* <img
                        src={Banner}
                        className="d-block w-100"
                        alt="Slide 1"
                    /> */}
                </header>

                {/* Carousel */}
                <div className="home-carousel">
                    <HomeCarousel />
                </div>

                {/* Sección de Información */}
                <div className="mx-auto p-4">
                    <Information />
                </div>

                {/* Footer */}
                <Footer />
            </div>
        </>
    );
}

export default Home;

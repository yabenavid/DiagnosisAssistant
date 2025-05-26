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
                <div className="description">
                    <h5>Cáncer de Estómago</h5>
                </div>
            
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

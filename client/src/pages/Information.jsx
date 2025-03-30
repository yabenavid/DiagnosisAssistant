import AmericanCancer from '../assets/american.png';
import InstitutoCancer from '../assets/national.png';
import '../styles/Home.css';

function Menu() {
    return (
        <>
            <div className="container mt-5">
                <section className="row">
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <img src={AmericanCancer} className="card-img-top" alt="Feature 1" />
                            <div className="card-body">
                                <h5 className="card-title">Cancer de Estómago</h5>
                                <p className="card-text"> Factores de riesgo, síntomas, cómo se detecta y cómo se trata.</p>
                                <a href="https://www.cancer.org/es/cancer/tipos/cancer-de-estomago.html" className="btn btn-primary">Ver mas</a>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <img src={InstitutoCancer} className="card-img-top" alt="Feature 2" />
                            <div className="card-body">
                                <h5 className="card-title">Cancer de Estómago</h5>
                                <p className="card-text">Diagnóstico del cáncer de estómago.</p>
                                <a href="https://www.cancer.gov/espanol/tipos/estomago/tratamiento" className="btn btn-primary">Ver mas</a>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card shadow-sm">
                            <img src="https://via.placeholder.com/300x200" className="card-img-top" alt="Feature 3" />
                            <div className="card-body">
                                <h5 className="card-title">Segmentación de Imágenes</h5>
                                <p className="card-text">Segment Anything By Meta Ai</p>
                                <a href="https://segment-anything.com/" className="btn btn-primary">Ver mas</a>
                            </div>
                        </div>
                    </div>
                </section>
            </div>

        </>
    )
}

export default Menu

import { useState } from 'react';
import GeneralImage from '../assets/fiet.png';
import FietImage from '../assets/banner4.png';
import FacultadImage from '../assets/banner3.png';
import '../styles/Home.css';

export function HomeCarousel() {
  return (
    <>
    
      <div id="carouselExampleCaptions" className="carousel slide w-100 vw-100 overflow-hidden" data-bs-ride="carousel">
        <div className="carousel-indicators">
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="0"
            className="active"
            aria-current="true"
            aria-label="Slide 1"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="1"
            aria-label="Slide 2"
          ></button>
          <button
            type="button"
            data-bs-target="#carouselExampleCaptions"
            data-bs-slide-to="2"
            aria-label="Slide 3"
          ></button>
        </div>
        <div className="carousel-inner">
          <div className="carousel-item active">
            <img
              src={GeneralImage}
              className="d-block w-100 img-fluid"
              alt="Slide 1"
            />
            {/* <div className="carousel-caption d-none d-md-block">
              <h5>FIET</h5>
              <p>60 Años</p>
            </div> */}
          </div>
          <div className="carousel-item">
            <img
              src={FietImage}
              className="d-block w-100 img-fluid"
              alt="Slide 2"
            />
            {/* <div className="carousel-caption d-none d-md-block">
              <h5>FIET</h5>
              <p>Facultad de Ingeniería Electrónica y Telecomunicaciones</p>
            </div> */}
          </div>
          <div className="carousel-item">
            <img
              src={FacultadImage}
              className="d-block w-100 img-fluid"
              alt="Slide 3"
            />
            {/* <div className="carousel-caption d-none d-md-block">
              <h5>Universidad del Cauca</h5>
              <p>Territorio de Paz</p>
            </div> */}
          </div>
        </div>
        <button
          className="carousel-control-prev"
          type="button"
          data-bs-target="#carouselExampleCaptions"
          data-bs-slide="prev"
        >
          <span className="carousel-control-prev-icon" aria-hidden="true"></span>
          <span className="visually-hidden">Previous</span>
        </button>
        <button
          className="carousel-control-next"
          type="button"
          data-bs-target="#carouselExampleCaptions"
          data-bs-slide="next"
        >
          <span className="carousel-control-next-icon" aria-hidden="true"></span>
          <span className="visually-hidden">Next</span>
        </button>
      </div>
    </>
  );
}

export default HomeCarousel;
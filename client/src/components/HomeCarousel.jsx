import { useState } from 'react'
import GeneralImage from '../assets/fiet.png'
import DoctorImage from '../assets/doctor.jpg'
import StomachImage from '../assets/stomach.jpg'


export function HomeCarousel() {
  return (
    <>
      <div id="carouselExampleCaptions" className="carousel slide" data-bs-ride="carousel">
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
              className="d-block w-100"
              alt="Slide 1"
            />
            <div className="carousel-caption d-none d-md-block">
              <h5>First Slide</h5>
              <p>This is the first slide's description.</p>
            </div>
          </div>
          <div className="carousel-item">
            <img
              src={DoctorImage}
              className="d-block w-100"
              alt="Slide 2"
            />
            <div className="carousel-caption d-none d-md-block">
              <h5>Second Slide</h5>
              <p>This is the second slide's description.</p>
            </div>
          </div>
          <div className="carousel-item">
            <img
              src={StomachImage}
              className="d-block w-100"
              alt="Slide 3"
            />
            <div className="carousel-caption d-none d-md-block">
              <h5>Third Slide</h5>
              <p>This is the third slide's description.</p>
            </div>
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
  )
}

export default HomeCarousel
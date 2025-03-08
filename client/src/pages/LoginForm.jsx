import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from 'axios';

// Components
import { HomeCarousel, Footer, NavigationBar } from "../components";

// CSS
import "/src/styles/LoginForm.css";

// APIs
import { ValidationUser } from "../api/login.api";

export function LoginForm() {
    const [formData, setFormData] = useState({ username: "", password: "" });
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // Conexion con la Api
    const handleSubmit = async (e) => {
        e.preventDefault(); // Evita la recarga de la página

        console.log("Formulario enviado:", formData);
        //navigate("/adminhome");
        // navigate("/diagnostic");
        try {
            // Llamada a la API
            const response = await ValidationUser(formData);

            console.log("Respuesta del servidor:", response);

            // Verifica si `response` contiene `data` y `is_admin`
            if (response?.data?.is_admin) {
                authorization(response?.data);
                navigate("/adminhome");
            } else {
                authorization(response?.data);
                navigate("/diagnostic");
            }
        } catch (error) {
            if (error.response && error.response.status === 401) {
                // Maneja el error 401 y muestra el mensaje
                alert(error.response.data.message);
            } else {
                console.error("Error en la validación:", error);
                alert("Ocurrió un error al validar. Intente nuevamente.");
            }
        }
    };

    const authorization = (data) => {
        // Initialize the access & refresh token in localstorage.      
        localStorage.clear();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('admin', data.is_admin);
        axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
    };

    return (
        <>
            <div>
                <NavigationBar />
                <div className="login-container">
                    <form className="login-form" onSubmit={handleSubmit}>
                        <h2 className="form-title">Iniciar Sesión</h2>

                        {/* username */}
                        <div className="form-group">
                            <label htmlFor="username">Correo Electrónico</label>
                            <input
                                type="username"
                                id="username"
                                name="username"
                                placeholder="Escribe tu correo"
                                value={formData.username}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        {/* Contraseña */}
                        <div className="form-group">
                            <label htmlFor="password">Contraseña</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                placeholder="Escribe tu contraseña"
                                value={formData.password}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        {/* Botón de Enviar */}
                        <button type="submit" className="btn-submit">
                            Ingresar
                        </button>

                        {/* Enlace de Recuperar Contraseña */}
                        <div className="form-footer">
                            <a href="#" className="forgot-password">
                                ¿Olvidaste tu contraseña?
                            </a>
                        </div>
                    </form>
                </div>
                <Footer />
            </div>
        </>
    );
}

export default LoginForm;

import { useState } from "react";
import { useNavigate } from "react-router-dom";

// Components
import { HomeCarousel, Footer, NavigationBar } from "../components";

// CSS
import "/src/styles/LoginForm.css";

// APIs
import { ValidationUser } from "../api/login.api";

export function LoginForm() {
    const [formData, setFormData] = useState({ email: "", password: "" });
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
        navigate("/diagnostic");
        // try {
        //     // Llamada a la API
        //     const response = await ValidationUser(formData);
            
        //     console.log("Respuesta del servidor:", response);

        //     // Verifica si `response` contiene `data` y `is_admin`
        //     if (response?.data?.is_admin) {
        //         navigate("/adminhome");
        //     } else {
        //         alert("Correo o contraseña inválidos, por favor ingréselos nuevamente.");
        //     }
        // } catch (error) {
        //     console.error("Error en la validación:", error);
        //     alert("Ocurrió un error al validar. Intente nuevamente.");
        // }
    };

    return (
        <>
            <div>
                <NavigationBar />
                <div className="login-container">
                    <form className="login-form" onSubmit={handleSubmit}>
                        <h2 className="form-title">Iniciar Sesión</h2>

                        {/* Email */}
                        <div className="form-group">
                            <label htmlFor="email">Correo Electrónico</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                placeholder="Escribe tu correo"
                                value={formData.email}
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

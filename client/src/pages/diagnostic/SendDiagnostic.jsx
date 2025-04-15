import React, { useState } from "react";
import { EmailsDiagnostic } from "../../api/diagnostic/senddiagnostic.api";
import { FcFeedback } from "react-icons/fc";
import '/src/styles/diagnostic/Diagnostic.css';

export const SendDiagnostic = () => {
    const [emails, setEmails] = useState([]);
    const [newEmail, setNewEmail] = useState("");
    const [validationMessage, setValidationMessage] = useState("");
    const [apiResponse, setApiResponse] = useState(null);

    const validateEmail = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    //TODO: al mandar los datos backen enviar el history_id y va en url, como PUT 

    
    const handleAddEmail = () => {
        if (emails.length >= 10) {
            setValidationMessage("Máximo 10 correos permitidos");
            return;
        }

        if (!validateEmail(newEmail)) {
            setValidationMessage("Formato de correo inválido");
            return;
        }

        if (emails.includes(newEmail)) {
            setValidationMessage("Este correo ya fue agregado");
            return;
        }

        setEmails([...emails, newEmail]);
        setNewEmail("");
        setValidationMessage("");
    };

    const handleRemoveEmail = (index) => {
        const updatedEmails = emails.filter((_, i) => i !== index);
        setEmails(updatedEmails);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (emails.length === 0) {
            setValidationMessage("Debe agregar al menos 1 correo");
            return;
        }

        try {
            const response = await EmailsDiagnostic(emails);
            setApiResponse({
                type: "success",
                message: "Correos enviados exitosamente"
            });
            setEmails([]);
        } catch (error) {
            setApiResponse({
                type: "error",
                message: error.response?.data?.message || "Error al enviar correos"
            });
        }
    };

    return (
        <div className="email-form-container">
            <h2>Enviar Resumen de Resultados</h2>
            
            {apiResponse && (
                <div className={`api-response ${apiResponse.type}`}>
                    {apiResponse.message}
                </div>
            )}

            <form onSubmit={(e) => e.preventDefault()}>
                <div className="input-group">
                    <input
                        type="email"
                        value={newEmail}
                        onChange={(e) => setNewEmail(e.target.value)}
                        placeholder="Ingrese correo electrónico"
                        className="email-input"
                    />
                    <button
                        type="button"
                        onClick={handleAddEmail}
                        className="add-button"
                        disabled={emails.length >= 10}
                    >
                        Agregar
                    </button>
                </div>
                
                {validationMessage && (
                    <div className="validation-message">{validationMessage}</div>
                )}

                <div className="email-list">
                    {emails.map((email, index) => (
                        <div key={index} className="email-item">
                            <span>{email}</span>
                            <button
                                type="button"
                                onClick={() => handleRemoveEmail(index)}
                                className="remove-button"
                            >
                                &times;
                            </button>
                        </div>
                    ))}
                </div>

                <button
                    type="submit"
                    onClick={handleSubmit}
                    className="submit-button"
                    disabled={emails.length === 0}
                >
                    Enviar Correos
                </button>

                <div className="email-counter">
                    {emails.length}/10 correos agregados
                </div>
            </form>
        </div>
    );
};

export default SendDiagnostic;
import React, { useState, useEffect } from "react";
import { NavigationBar, Footer } from "../../components";
import { handleSelectFolderDiagnostic } from "../../hooks/UploadImages";
import { useNavigate } from "react-router-dom";
import { SegmentImages } from "../../api/diagnostic/diagnostic.api";
import '/src/styles/diagnostic/Diagnostic.css';

const Diagnostic = () => {
    const navigate = useNavigate();
    const [folderName, setFolderName] = useState("");
    const [imageCount, setImageCount] = useState(0);
    const [imageList, setImageList] = useState([]);
    const [resultData, setResultData] = useState(null);

    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        }
    }, [navigate]);

    const handleUpload = async () => {
        if (imageList.length === 0) {
            alert("No hay imágenes para enviar. Selecciona otra carpeta.");
            return;
        }

        const formData = new FormData();
        imageList.forEach((img) => {
            formData.append("images", img.file);
        });
        formData.append("segment_model", 1);

        try {
            const response = await SegmentImages(formData);
            if (response?.status === 200) {
                // Validación adicional de la respuesta
                const responseData = response.data || {};
                console.log("Respuesta del servidor:", response.data);

                // Guardar los resultados en el estado
                setResultData(responseData.results || []); // results es un array

                // Limpiar estados
                setFolderName("");
                setImageCount(0);
                setImageList([]);
            } else {
                alert(response?.data?.message || "Ocurrió un error desconocido");
            }
        } catch (error) {
            console.error("Error al subir las imágenes:", error);
            alert("Error al subir las imágenes.");
        }
    };

    return (
        <div>
            <NavigationBar />

            <div className="diagnostic-container">
                <h2>Seleccionar Carpeta de Imágenes</h2>
                <button
                    onClick={() =>
                        handleSelectFolderDiagnostic(setFolderName, setImageCount, setImageList)
                    }
                >
                    Seleccionar Carpeta
                </button>

                {folderName && (
                    <p>
                        📁 Carpeta seleccionada: <strong>{folderName}</strong>
                    </p>
                )}

                {imageCount > 0 && (
                    <p>
                        📷 Imágenes encontradas: <strong>{imageCount} (Máx: 3)</strong>
                    </p>
                )}

                {imageList.length > 0 && (
                    <div className="image-preview-container">
                        {imageList.map((img, index) => (
                            <div key={index} className="image-thumbnail">
                                <img
                                    src={img.url}
                                    alt={img.name}
                                    className="thumbnail-image"
                                />
                                <p className="image-name">{img.name}</p>
                            </div>
                        ))}
                    </div>
                )}

                <button
                    onClick={handleUpload}
                    disabled={imageList.length === 0}
                    className="evaluate-button"
                >
                    Evaluar
                </button>

                {resultData && resultData.length > 0 && (
                    <div className="result-container">
                        {resultData.map((result, index) => (
                            <div key={index} className="result-card">
                                <div
                                    className="percentage-circle"
                                    style={{
                                        background: `conic-gradient(
                                            #6dcca3 ${result.average_similarity_percentage}%,
                                            #9155a7 ${result.average_similarity_percentage}% 100%
                                        )`,
                                    }}
                                >
                                    <span>{result.average_similarity_percentage.toFixed(1)}%</span>
                                </div>

                                <div className="diagnosis-message">
                                    <h3>Resultado del Diagnóstico</h3>
                                    <p className="message-content">{result.diagnosis_message}</p>
                                </div>

                                {result.pacient_image && (
                                    <div className="patient-image-section">
                                        <h3>Imagen del Paciente</h3>
                                        <img
                                            src={result.pacient_image}
                                            alt="Imagen médica"
                                            className="medical-image"
                                        />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <Footer />
        </div>
    );
};

export default Diagnostic;
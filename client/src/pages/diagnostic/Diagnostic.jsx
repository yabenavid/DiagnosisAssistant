import React, { useState, useEffect } from "react";
import { NavigationBar, Footer, SegmentationTypeSelector } from "../../components";
import { SendDiagnostic } from "./SendDiagnostic";
import { handleSelectFolderDiagnostic } from "../../hooks/UploadImages";
import { useNavigate } from "react-router-dom";
import { SegmentImages } from "../../api/diagnostic/diagnostic.api";
import { FcFeedback, FcFolder, FcFinePrint, FcRefresh } from "react-icons/fc";
import '/src/styles/diagnostic/Diagnostic.css';
import { useAuth } from "../../context/AuthContext";

const Diagnostic = () => {

    const { auth } = useAuth();
    const navigate = useNavigate();
    const [folderName, setFolderName] = useState("");
    const [imageCount, setImageCount] = useState(0);
    const [imageList, setImageList] = useState([]);
    const [resultData, setResultData] = useState(null);
    const [selectedImage, setSelectedImage] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [typeImage, setTypeImage] = useState(0);
    const [showNotification, setShowNotification] = useState(false);
    const [showEmailModal, setShowEmailModal] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedOption, setSelectedOption] = useState("");


    useEffect(() => {
        if (!localStorage.getItem('access_token')) {
            navigate("/login");
        }
    }, [navigate]);

    useEffect(() => {
        if (resultData && resultData.length > 0) {
            setShowNotification(true);
            const timer = setTimeout(() => {
                setShowNotification(false);
            }, 10000);
            return () => clearTimeout(timer);
        }
    }, [resultData]);

    const handleUpload = async () => {
        if (!selectedOption) {
            alert("Debe seleccionar un tipo de segmentación antes de analizar.");
            return;
        }
        if (imageList.length === 0) {
            alert("No hay imágenes para enviar. Selecciona otra carpeta.");
            return;
        }

        setIsLoading(true);
        const formData = new FormData();
        imageList.forEach((img) => {
            formData.append("images", img.file);
        });
        formData.append("segment_model", selectedOption);

        try {
            const response = await SegmentImages(formData, auth.accessToken);
            if (response?.status === 200) {
                localStorage.setItem('history_id', response.data.history_id || '');
                const responseData = response.data || {};
                setResultData(responseData.results || []);
                setFolderName("");
                setImageCount(0);
                setImageList([]);
            } else {
                alert(response?.data?.message || "Ocurrió un error desconocido");
            }
        } catch (error) {
            console.error("Error al subir las imágenes:", error);
            alert("Error al subir las imágenes.");
        } finally {
            setIsLoading(false);
        }
    };

    const getAllImages = () => {
        return resultData.flatMap(result =>
            result.pacient_image ? [`data:image/png;base64,${result.pacient_image}`] : []
        );
    };

    const getImagesSegmented = () => {
        return resultData.flatMap(result =>
            result.segmented_pacient_image ? [`data:image/png;base64,${result.segmented_pacient_image}`] : []
        );
    };

    const openImageModal = (imageSrc, index, type) => {
        setSelectedImage(imageSrc);
        setCurrentImageIndex(index);
        setIsModalOpen(true);
        setTypeImage(type);
    };

    const navigateImages = (direction) => {
        const allImages = typeImage === 0 ? getAllImages() : getImagesSegmented();
        const newIndex = (currentImageIndex + direction + allImages.length) % allImages.length;
        setCurrentImageIndex(newIndex);
        setSelectedImage(allImages[newIndex]);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedImage(null);
        setCurrentImageIndex(0);
    };

    return (
        <>
            <div className="diagnostic-page">
                <NavigationBar />

                {isLoading && (
                    <div className="loading-overlay">
                        <div className="loading-container">
                            <img
                                src="/src/assets/cargando.gif"
                                alt="Cargando..."
                                className="loading-gif"
                            />
                            <p>Procesando imágenes, por favor espere...</p>
                        </div>
                    </div>
                )}

                {showNotification && (
                    <div className="notification">
                        <span>📬 El informe diagnóstico ha sido enviado exitosamente a su correo electrónico</span>
                        <button
                            onClick={() => setShowNotification(false)}
                            className="close-notification"
                        >
                            ×
                        </button>
                    </div>
                )}


                <div className="description">
                    <h3>Asistente de Diagnóstico</h3>
                </div>
                <div className="diagnostic-container">

                    {/* Solo muestra el selector y el botón si NO hay resultados */}
                    {(!resultData || resultData.length === 0) && (
                        <>
                            <h4>Seleccione el tipo de segmentación</h4><br />
                            <SegmentationTypeSelector
                                selectedOption={selectedOption}
                                setSelectedOption={setSelectedOption}
                            />
                            <h4>Seleccione la carpeta con imágenes</h4>
                            <div className="action-buttons">
                                <button
                                    onClick={() => {
                                        setResultData(null);
                                        handleSelectFolderDiagnostic(setFolderName, setImageCount, setImageList);
                                    }}
                                >
                                    <FcFolder /> Seleccionar
                                </button>

                                {folderName && (
                                    <p>📁 Carpeta seleccionada: <strong>{folderName}</strong></p>
                                )}

                                {imageCount > 0 && (
                                    <p>📷 Imágenes encontradas: <strong>{imageCount} (Máx: 3)</strong></p>
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
                                    disabled={imageList.length === 0 || isLoading}
                                    className="evaluate-button"
                                >
                                    <FcFinePrint /> {isLoading ? 'Procesando...' : 'Analizar'}
                                </button>
                            </div>
                        </>
                    )}

                    {resultData && resultData.length > 0 && (
                        <div className="result-container">
                            {resultData.map((result, index) => (
                                <div key={index} className="result-card">
                                    <div className="percentage-circle" style={{
                                        background: `conic-gradient(
                                            #6dcca3 ${result.average_similarity_percentage}%,
                                            #9155a7 ${result.average_similarity_percentage}% 100%
                                        )`
                                    }}>
                                        <span>{result.average_similarity_percentage?.toFixed(1)}%</span>
                                    </div>

                                    <div className="diagnosis-message">
                                        <h3>Resultado del Diagnóstico</h3>
                                        <p className="message-content">{result.diagnosis_message}</p>
                                    </div>

                                    {result.pacient_image && (
                                        <div className="patient-image-section">
                                            <div className="text-image"><p>Imagen del Paciente</p></div>
                                            <img
                                                src={`data:image/png;base64,${result.pacient_image}`}
                                                alt="Imagen médica"
                                                className="medical-image"
                                                onClick={() => openImageModal(
                                                    `data:image/png;base64,${result.pacient_image}`,
                                                    index,
                                                    0
                                                )}
                                            />
                                        </div>
                                    )}

                                    {result.segmented_pacient_image && (
                                        <div className="patient-image-section">
                                            <div className="text-image"><p>Imagen Segmentada</p></div>
                                            <img
                                                src={`data:image/png;base64,${result.segmented_pacient_image}`}
                                                alt="Imagen procesada"
                                                className="medical-image"
                                                onClick={() => openImageModal(
                                                    `data:image/png;base64,${result.segmented_pacient_image}`,
                                                    index,
                                                    1
                                                )}
                                            />
                                        </div>
                                    )}
                                </div>
                            ))}

                            <button
                                onClick={() => setShowEmailModal(true)}
                                className="send-emails-button"
                            >
                                <FcFeedback /> Compartir resumen de resultados
                            </button>

                            <button
                                className="evaluate-again-button"
                                onClick={() => {
                                    setResultData(null);
                                    setFolderName("");
                                    setImageCount(0);
                                    setImageList([]);
                                }}
                            >
                                <FcRefresh /> Volver a evaluar
                            </button>
                        </div>
                    )}

                    {isModalOpen && (
                        <div className="image-modal" onClick={closeModal}>
                            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                                <span className="close-button" onClick={closeModal}>&times;</span>
                                <img
                                    src={selectedImage}
                                    className="modal-image"
                                    alt="Imagen ampliada"
                                />
                                <div className="navigation-buttons">
                                    <button
                                        className="nav-arrow prev"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            navigateImages(-1);
                                        }}
                                    >
                                        &#10094;
                                    </button>
                                    <button
                                        className="nav-arrow next"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            navigateImages(1);
                                        }}
                                    >
                                        &#10095;
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {showEmailModal && (
                        <div className="email-modal-overlay" onClick={() => setShowEmailModal(false)}>
                            <div className="email-modal-content" onClick={(e) => e.stopPropagation()}>
                                <button
                                    className="close-email-modal"
                                    onClick={() => setShowEmailModal(false)}
                                >
                                    &times;
                                </button>
                                <SendDiagnostic />
                            </div>
                        </div>
                    )}
                </div>
            </div>
            <Footer />
        </>
    );
};

export default Diagnostic;
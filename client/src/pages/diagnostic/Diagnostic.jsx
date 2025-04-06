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
    const [selectedImage, setSelectedImage] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [typeImage, setTypeImage] = useState(0);

    useEffect(() => {
        if (!localStorage.getItem('access_token')) {
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
                const responseData = response.data || {};
                console.log("Respuesta del servidor:", response.data);
                
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
        if (typeImage === 0) {
        const allImages = getAllImages();
        const newIndex = (currentImageIndex + direction + allImages.length) % allImages.length;
        setCurrentImageIndex(newIndex);
        setSelectedImage(allImages[newIndex]);
        }else {
            const allImages = getImagesSegmented();
            const newIndex = (currentImageIndex + direction + allImages.length) % allImages.length;
            setCurrentImageIndex(newIndex);
            setSelectedImage(allImages[newIndex]);
        }

    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedImage(null);
        setCurrentImageIndex(0);
    };

    return (
        <div>
            <NavigationBar />

            <div className="diagnostic-container">
                <h2>Seleccionar Carpeta de Imágenes</h2>
                <button
                    onClick={() => {
                        setResultData(null);
                        handleSelectFolderDiagnostic(setFolderName, setImageCount, setImageList);
                    }}
                >
                    Seleccionar Carpeta
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
                    disabled={imageList.length === 0}
                    className="evaluate-button"
                >
                    Evaluar
                </button>

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
                                        <div className="text-image"> <p>Imagen del Paciente</p></div>
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
                                        <div className="text-image"> <p>Imagen del Asistente</p></div>
                                        <img
                                            src={`data:image/png;base64,${result.segmented_pacient_image}`}
                                            alt="Imagen médica"
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
            </div>

            <Footer />
        </div>
    );
};

export default Diagnostic;
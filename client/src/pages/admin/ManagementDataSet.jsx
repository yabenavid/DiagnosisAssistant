import React, { useEffect, useState, Suspense } from "react";
import { useNavigate } from "react-router-dom";

import { NavigationBar, Footer, SegmentationTypeSelector } from "../../components";
import { handleSelectFolder } from "../../hooks/UploadImages";
import { FcFolder, FcUp } from "react-icons/fc";

//APis
import { addDataSet, getCountDataSet } from "../../api/admin/dataset.api";
import { useAuth } from "../../context/AuthContext";

//Css
import '/src/styles/admin/ManagementDataSet.css';

/**
 * Componente para la gestión de datasets de imágenes.
 * Permite seleccionar un modelo de segmentación y cargar un archivo ZIP con imágenes.
 */
const ManagementDataSet = () => {
    const navigate = useNavigate();
    const { auth } = useAuth();
    const [folderName, setFolderName] = useState("");
    const [zipFile, setZipFile] = useState(null);
    const [imageCount, setImageCount] = useState(0);
    const [qtyDataSet, setDatasetCount] = useState(0);
    const [selectedOption, setSelectedOption] = useState("");

    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        } else {
            countDataset();
        }
    }, []);

    /**
     * Subir archivo ZIP al servidor
     */
    const handleUpload = async () => {
        if (!selectedOption) {
            alert("Debe seleccionar un modelo de segmentación.");
            return;
        }
        if (!zipFile || imageCount === 0) {
            alert("No hay imágenes para enviar. Selecciona otra carpeta.");
            return;
        }

        const formData = new FormData();
        formData.append("zip_file", zipFile, `${folderName}.zip`);
        formData.append("segment_model", selectedOption);

        try {
            const response = await addDataSet(formData, auth.accessToken);
            if (response?.status === 200) {
                alert(response?.data?.message);
                await countDataset();

                // Resetear los estados para limpiar el formulario
                setFolderName("");
                setZipFile(null);
                setImageCount(0);
            } else {
                alert(response.data.message);
            }

            console.log("Respuesta del servidor:", response.data);
        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert(error.response.data.message);
        }
    };

    /**
     * Función para contar la cantidad de imágenes en el dataset.
     */
    const countDataset = async () => {
        try {
            const response = await getCountDataSet(auth.accessToken);
            setDatasetCount(response?.data);

        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert("Error al subir la carpeta.");
        }
    };

    return (
        <>
            <Suspense fallback="Cargando Traducciones">
                <div className="management-dataset-container">
                    <div className="description">
                        <h3>Gestión Banco de Imagénes</h3>
                    </div>
                    <NavigationBar />
                    <div className="management-dataset-flex">
                        <div className="count-data-set">
                            <h3>Cantidad de Imágenes</h3>
                            <strong>Sam {qtyDataSet}</strong>
                            <strong>Scikit {qtyDataSet}</strong>
                        </div>
                        <div className="management-dataset-content">
                            <h4>Seleccione un modelo de segmentación</h4><br />
                            <SegmentationTypeSelector
                                selectedOption={selectedOption}
                                setSelectedOption={setSelectedOption}
                            />

                            <div style={{ padding: "20px", textAlign: "center" }}>
                                <h4>Seleccionar Carpeta de Imágenes</h4>
                                <button onClick={() => handleSelectFolder(setFolderName, setImageCount, setZipFile)}>
                                    <FcFolder /> Seleccionar
                                </button>

                                {folderName && <p>📁 Carpeta seleccionada: <strong>{folderName}</strong></p>}
                                {imageCount > 0 && <p>📷 Imágenes encontradas: <strong>{imageCount}</strong></p>}

                                <button
                                    onClick={handleUpload} disabled={!zipFile }>
                                    <FcUp /> Cargar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </Suspense>
            <Footer />
        </>
    );
};

export default ManagementDataSet;

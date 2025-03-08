import React, { useEffect, useState, Suspense } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { useNavigate } from "react-router-dom";

import { NavigationBar, Footer } from "../../components";
import { handleSelectFolder } from "../../hooks/UploadImages";

//APis
import { addDataSet, getCountDataSet } from "../../api/admin/dataset.api";

const ManagementDataSet = () => {
    const navigate = useNavigate();

    const [folderName, setFolderName] = useState("");
    const [zipFile, setZipFile] = useState(null);
    const [imageCount, setImageCount] = useState(0); // Contador de imágenes
    const [qtyDataSet, setDatasetCount] = useState(0);

    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        } else {
            countDataset();
        }
    }, []);

    const topCenter = (message) => {
        toast.info(message, {
            position: 'top-center',
            autoClose: 3000
        });
    };

    // Subir archivo ZIP al servidor
    const handleUpload = async () => {

        if (!zipFile || imageCount === 0) {
            alert("No hay imágenes para enviar. Selecciona otra carpeta.");
            return;
        }

        const formData = new FormData();
        formData.append("zip_file", zipFile, `${folderName}.zip`);

        try {
            const response = await addDataSet(formData);
            if (response?.status === 200) {
                alert(response?.data?.message);
                //topCenter(response?.data?.message);
                await countDataset();

                // Resetear los estados para limpiar el formulario
                setFolderName("");
                setZipFile(null);
                setImageCount(0);
            } else {
                // toast.error(response?.data?.message || "Ocurrió un error", {
                //     position: "top-right",
                //     autoClose: 5000, // Se cierra en 5 segundos
                // });
                alert(response.data.message);
            }

            console.log("Respuesta del servidor:", response.data);
        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert(error.response.data.message);
        }
    };

    // Cantidad de imagenes en el dataSet
    const countDataset = async () => {
        try {
            const response = await getCountDataSet();
            setDatasetCount(response?.data);

        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert("Error al subir la carpeta.");
        }
    };

    return (
        <Suspense fallback="Cargando Traducciones">
            <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
                <NavigationBar />
                <h1>Gestión de Doctores</h1>
                <div className="count-data-set">
                    <h3>Cantidad de imagenes en el data Set</h3>
                    <strong>Cantidad: {qtyDataSet}</strong>
                </div>

                <div style={{ padding: "20px", textAlign: "center" }}>
                    <h2>Seleccionar Carpeta de Imágenes</h2>
                    <button onClick={() => handleSelectFolder(setFolderName, setImageCount, setZipFile)}>
                        Seleccionar Carpeta
                    </button>

                    {folderName && <p>📁 Carpeta seleccionada: <strong>{folderName}</strong></p>}
                    {imageCount > 0 && <p>📷 Imágenes encontradas: <strong>{imageCount}</strong></p>}

                    <button onClick={handleUpload} disabled={!zipFile} style={{ marginTop: "10px" }}>
                        Subir DataSet
                    </button>
                </div>
                <Footer />
            </div>
        </Suspense>
    );
};

export default ManagementDataSet;

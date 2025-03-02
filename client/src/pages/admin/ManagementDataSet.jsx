import React, { useEffect, useState } from "react";
import { ToastContainer, toast } from 'react-toastify';

import { NavigationBar, Footer } from "../../components";
import { handleSelectFolder } from "../../hooks/UploadImages";

//APis
import { addDataSet, getCountDataSet } from "../../api/admin/dataset.api";

const ManagementDataSet = () => {

    const [folderName, setFolderName] = useState("");
    const [zipFile, setZipFile] = useState(null);
    const [imageCount, setImageCount] = useState(0); // Contador de imágenes
    const [qtyDataSet, setDatasetCount] = useState(0);

    useEffect(() => {
        countDataset();
    });

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
        formData.append("file", zipFile, `${folderName}.zip`);

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
                toast.error(response?.data?.message || "Ocurrió un error", {
                    position: "top-right",
                    autoClose: 5000, // Se cierra en 5 segundos
                });
            }

            console.log("Respuesta del servidor:", response.data);
        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert("Error al subir la carpeta.");
        }
    };

    // Cantidad de imagenes en el dataSet
    const countDataset = async () => {
        try {
            const response = await getCountDataSet();
            setDatasetCount(response?.data?.count);

        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert("Error al subir la carpeta.");
        }
    };

    return (
        <div>
            <NavigationBar />
            <div className="count-data-set" >
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
            <Footer></Footer>
        </div>
    );
};

export default ManagementDataSet;

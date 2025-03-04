import React, { useState } from "react";
import { NavigationBar, Footer } from "../../components";
import { handleSelectFolderDiagnostic } from "../../hooks/UploadImages";
import { useEffect} from "react";
import { useNavigate } from "react-router-dom";

//APIs
import { addDataSet } from "../../api/admin/dataset.api";

const Diagnostic = () => {
    
    const navigate = useNavigate();
    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        }
    }, []);

    const [folderName, setFolderName] = useState("");
    const [zipFile, setZipFile] = useState(null);
    const [imageCount, setImageCount] = useState(0);
    const [imageList, setImageList] = useState([]);

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

                // Resetear los estados para limpiar el formulario
                setFolderName("");
                setZipFile(null);
                setImageCount(0);
                setImageList([]); // Limpiar la lista de imágenes
            } else {
                alert(response?.data?.message || "Ocurrió un error.");
            }

            console.log("Respuesta del servidor:", response.data);
        } catch (error) {
            console.error("Error al subir la carpeta:", error);
            alert("Error al subir la carpeta.");
        }
    };

    return (
        <div>
            <NavigationBar />

            <div style={{ padding: "20px", textAlign: "center" }}>
                <h2>Seleccionar Carpeta de Imágenes</h2>
                <button onClick={() => handleSelectFolderDiagnostic(setFolderName, setImageCount, setZipFile, setImageList)}>
                    Seleccionar Carpeta
                </button>
                {console.log(setImageList)}
                {folderName && <p>📁 Carpeta seleccionada: <strong>{folderName}</strong></p>}
                {imageCount > 0 && <p>📷 Imágenes encontradas: <strong>{imageCount} (Máx: 10)</strong></p>}

                {/*Mostrar las imágenes seleccionadas */}
                {imageList.length > 0 && (
                    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", marginTop: "10px" }}>

                        {imageList.map((img, index) => (
                            <div key={index} style={{ margin: "5px" }}>
                                <img
                                    src={img.url}
                                    alt={img.name}
                                    style={{ width: "100px", height: "100px", objectFit: "cover", borderRadius: "5px" }}
                                />
                                <p style={{ fontSize: "12px" }}>{img.name}</p>
                            </div>
                        ))}
                    </div>
                )}

                <button onClick={handleUpload} disabled={!zipFile} style={{ marginTop: "10px" }}>
                    Evaluar
                </button>
            </div>

            <Footer />
        </div>
    );
};

export default Diagnostic;

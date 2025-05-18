import React, { useState, useEffect, Suspense } from 'react';
import { NavigationBar, Footer } from "../../components";
import { getHistory } from "../../api/diagnostic/history.api";
import '/src/styles/diagnostic/history.css';
import { FcDownload, FcInfo } from "react-icons/fc";
import { useAuth } from "../../context/AuthContext";

/**
 * Historial de registros de resultados. 
 */
const History = () => {

    const { auth } = useAuth();
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState(1);
    const rowsPerPage = 10;

    const indexOfLastRow = currentPage * rowsPerPage;
    const indexOfFirstRow = indexOfLastRow - rowsPerPage;
    const currentHistory = data.slice(indexOfFirstRow, indexOfLastRow);
    const paginate = (pageNumber) => setCurrentPage(pageNumber);


    useEffect(() => {
        if (localStorage.getItem('access_token') === null) {
            navigate("/login");
        } else {
            fetchHistory();
        }
    }, []);

    const fetchHistory = async () => {
        try {

            const response = await getHistory(auth.accessToken);

            if (response?.status === 200) {
                console.log("Data:", response?.data);
                setData(response?.data || []);
            } else {
                console.error("Error en la respuesta de la API:", response);
                setData([]);
            }
        } catch (error) {
            console.error('Error fetching history:', error);
            alert('Error al cargar el historial');
            setData([]);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        const options = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    const renderHistories = () => {
        return (
            <div className="history-table-wrapper">
            <div style={{ marginTop: "20px" }}>
                <h2>Resultados</h2>
                {data.length === 0 ? (
                    <p>No hay registros.......</p>
                ) : (
                    <>
                        <table border="1" style={{ width: "100%", textAlign: "left" }}>
                            <thead>
                                <tr>
                                    <th>Id</th>
                                    <th>Fecha Creación</th>
                                    <th>Nombre</th>
                                    <th>Acción</th>

                                </tr>
                            </thead>
                            <tbody>
                                {currentHistory.map((history, index) => (
                                    <tr key={index}>
                                        <td>{history.id}</td>
                                        <td>{formatDate(history.created_at)}</td>
                                        <td>{history.filename}</td>
                                        <td className="files-column">
                                            {/* Botón de descargar */}
                                            <div className="tooltip-container">
                                                <button
                                                    onClick={() => window.open(history.download_url, "_blank")} // Abre el enlace en una nueva pestaña
                                                    style={{ marginRight: "10px" }}
                                                >
                                                    <FcDownload /> {/* Ícono de edición */}
                                                </button>
                                                <span className="tooltip-text"><FcInfo /> Descargar</span>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {/* Controles de paginación */}
                        <div className="pagination">
                            {Array.from({ length: Math.ceil(data.length / rowsPerPage) }, (_, i) => (
                                <button
                                    key={i}
                                    onClick={() => paginate(i + 1)}
                                    className={currentPage === i + 1 ? "active" : ""}
                                >
                                    {i + 1}
                                </button>
                            ))}
                        </div>

                    </>
                )}
            </div>
            </div>
        );
    };

    return (
        <>
            <Suspense fallback="Cargando Traducciones">
                <div className="history-container">
                    <NavigationBar />

                    <div className="history-content">
                        <div className="description">
                            <h3>Historial</h3>
                        </div>

                        {loading ? (
                            <div className="loading-message">
                                <p>Cargando historial...</p>

                            </div>

                        ) : (
                            <>
                                {data.length === 0 ? (
                                    <div className="records-message">
                                        <p>No hay registros.</p>
                                    </div>
                                ) : (
                                    renderHistories()
                                )}
                            </>
                        )}
                    </div>

                </div>
                <Footer />
            </Suspense>
        </>
    );
};

export default History;
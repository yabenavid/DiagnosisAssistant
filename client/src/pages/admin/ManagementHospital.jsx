import React, { useEffect, useState, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import { NavigationBar, Footer } from '../../components';
import { useTranslation } from "react-i18next";
import { FaEdit, FaPlus, FaList } from 'react-icons/fa';
import { FcEmptyTrash, FcInfo } from "react-icons/fc";
import CryptoJS from "crypto-js";
import '/src/styles/admin/Management.css';
import { getListHospital, updateHospital, deleteHospital, addHospital } from "../../api/admin/hospital.api";
import { useAuth } from "../../context/AuthContext";

/**
 * Componente para la gestión de hospitales. 
 */
const ManagementHospital = () => {
  const ENCRYPTION_KEY = "my-secure-key";
  const { auth } = useAuth();
  const navigate = useNavigate();
  
  const [hospitales, setHospital] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentHospitalId, setCurrentHospitalId] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const { t: translate } = useTranslation();

  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  const indexOfLastRow = currentPage * rowsPerPage;
  const indexOfFirstRow = indexOfLastRow - rowsPerPage;
  const currentHospitals = hospitales.slice(indexOfFirstRow, indexOfLastRow);
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    address: "",
    phone: ""
  });

  useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      navigate("/login");
    } else {
      getList();
    }
  }, []);

  /**
   * Controlador de eventos para manejar los cambios en el formulario.
   * @param {*} e 
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  /**
   * Elimina un hospital de la lista.
   * @param {*} id 
   */
  const handleDelete = async (id) => {
    const confirmed = window.confirm(translate("deleteregister"));

    if (confirmed) {
      try {
        const response = await deleteHospital(id, auth.accessToken);

        if (response?.status === 200) {
          alert(response?.data?.message);
          getList();
        } else {
          alert(response?.data?.message);
        }
      } catch (error) {
        console.error("Error al eliminar el hospital:", error);
        alert(translate("errordeleted"));
      }
    }
  };

  /**
   * Edita un hospital existente.
   * @param {*} id 
   */
  const handleEdit = (id) => {
    const hospital = hospitales.find((hospital) => hospital.id === id);
    if (hospital) {
      setFormData(hospital);
      setCurrentHospitalId(id);
      setIsEditing(true);
      setShowForm(true);
    } else {
      console.error("Hospital no encontrado");
    }
  };

  /**
   * Muestra el formulario para agregar un nuevo hospital.
   */
  const handleAddNewHospital = () => {
    setFormData({
      id: "",
      name: "",
      address: "",
      phone: ""
    });
    setIsEditing(false);
    setShowForm(true);
  };

  /**
   * Envio de datos al servidor para registrar o editar un hospital.
   * @param {*} e 
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convertir los datos en JSON y encriptarlos
    const jsonData = JSON.stringify(formData);

    const encryptedData = CryptoJS.AES.encrypt(jsonData, ENCRYPTION_KEY).toString();
    try {
      if (isEditing) {
        const response = await updateHospital(currentHospitalId, jsonData, auth.accessToken);

        if (response.status === 200) {
          alert(response?.data?.message);
          setIsEditing(false);
        }
      } else {
        // Agregar nuevo Hospital
        const response = await addHospital(jsonData, auth.accessToken);
        if (response.status === 200) {
          alert(response?.data.message);
        }
      }
    } catch (error) {
      const message = error.response?.data?.message ?? translate("errorupdate");
      if (isEditing) {
        console.error("Error al actualizar el doctor:", error);
        alert(message);
      } else {
        console.error("Error al crear el doctor:", error);
        alert(message);
      }
    }

    setShowForm(false);
    cleanFormData();
    await getList();

  };

  /**
   * Limpia los datos del formulario después de enviar o cancelar.
   */
  const cleanFormData = () => {
    setFormData({
      id: "",
      name: "",
      address: "",
      phone: ""
    });
  };

  /**
   * Obtiene la lista de hospitales registrados.
   */
  const getList = async () => {
    try {
      const response = await getListHospital(auth.accessToken);
      setHospital(response?.data?.hospitals);
    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  /**
   * Renderiza la lista de hospitales en una tabla.
   */
  const renderHospitals = () => {
    return (
      <div className="history-table-wrapper">
        <h2>Registros</h2>
        {hospitales.length === 0 ? (
          <p>No hay Hospitales registrados.</p>
        ) : (
          <>
            <table border="1" style={{ width: "100%", textAlign: "left" }}>
              <thead>
                <tr>
                  <th>Id</th>
                  <th>Nombre</th>
                  <th>Dirección</th>
                  <th>Teléfono</th>
                  <th className="files-column">Acción</th>
                </tr>
              </thead>
              <tbody>
                {currentHospitals.map((hospital, index) => (
                  <tr key={index}>
                    <td>{hospital.id}</td>
                    <td>{hospital.name}</td>
                    <td>{hospital.address}</td>
                    <td>{hospital.phone}</td>
                    <td className="files-column">
                      {/* Botón de editar con tooltip */}
                      <div className="tooltip-container">
                        <button onClick={() => handleEdit(hospital.id)} style={{ marginRight: "10px" }}>
                          <FaEdit />
                        </button>
                        <span className="tooltip-text"><FcInfo /> Editar</span>
                      </div>
                      {/* Botón de eliminar con tooltip */}
                      <div className="tooltip-container">
                        <button onClick={() => handleDelete(hospital.id)}>
                          <FcEmptyTrash />
                        </button>
                        <span className="tooltip-text"><FcInfo /> Eliminar</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Controles de paginación */}
            <div className="pagination">
              {Array.from({ length: Math.ceil(hospitales.length / rowsPerPage) }, (_, i) => (
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
    );
  };

  return (
    <>
      <Suspense fallback="Cargando Traducciones">
        <div className="management-medical-container">
          <div className="description">
            <h3>Gestión Hospitales</h3>
          </div>
          <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <NavigationBar />

            <div className="action-buttons">
              <button onClick={handleAddNewHospital} style={{ marginRight: "10px" }}>
                <FaPlus /> Agregar
              </button>
              <button onClick={() => setShowForm(false)}>
                <FaList /> Ver Todos
              </button>
            </div>

            {showForm && (
              <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "0 auto" }}>
                <h2>{isEditing ? "Editar Hospital" : "Registrar Nuevo Hospital"}</h2>

                <div style={{ marginBottom: "15px" }}>
                  <label>
                    {translate("name")}<span className="required">*</span>
                  </label>
                  <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                </div>

                <div style={{ marginBottom: "15px" }}>
                  <label>
                    {translate("address")}<span className="required">*</span>
                  </label>
                  <input type="text" name="address" value={formData.address} onChange={handleChange} required />
                </div>

                <div style={{ marginBottom: "15px" }}>
                  <label>
                    {translate("phone")}<span className="required">*</span>
                  </label>
                  <input type="text" name="phone" value={formData.phone} onChange={handleChange} required />
                </div>

                <button type="submit">{isEditing ? "Actualizar" : "Registrar"}</button>
              </form>
            )}

            {!showForm && renderHospitals()}
          </div>
        </div>
        <Footer />
      </Suspense>
    </>
  );
};

export default ManagementHospital;

import React, { useEffect, useState, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import { NavigationBar, Footer } from '../../components';
import { useTranslation } from "react-i18next";
import { FaEdit, FaPlus, FaList } from 'react-icons/fa';
import { FcEmptyTrash, FcInfo } from "react-icons/fc";

import '/src/styles/admin/Management.css';

// APIs
import { getListHospital, updateHospital, deleteHospital, addHospital } from "../../api/admin/hospital.api";

const ManagementHospital = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    id: "",
    name: "",
    address: "",
    phone: ""
  });

  const [hospitales, setHospital] = useState([]); // Lista de hospitales registrados
  const [isEditing, setIsEditing] = useState(false); // Indica si estamos editando
  const [currentHospitalId, setCurrentHospitalId] = useState(null); // Hospital en edición
  const [showForm, setShowForm] = useState(false); // Mostrar/ocultar formulario
  const { t: translate } = useTranslation();

  const [currentPage, setCurrentPage] = useState(1); // Página actual
  const rowsPerPage = 10; // Número de filas por página

  useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      navigate("/login");
    } else {
      getList();
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleDelete = async (id) => {
    const confirmed = window.confirm(translate("deleteregister"));

    if (confirmed) {
      try {
        const response = await deleteHospital(id);

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

  const handleEdit = (id) => {
    const hospital = hospitales.find((hospital) => hospital.id === id);
    if (hospital) {
      setFormData(hospital);
      setCurrentHospitalId(id);
      setIsEditing(true);
      setShowForm(true); // Mostrar el formulario para edición
    } else {
      console.error("Hospital no encontrado");
    }
  };

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

  const getList = async () => {
    try {
      const response = await getListHospital();
      setHospital(response?.data?.hospitals);
    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  // Calcular los hospitales a mostrar en la página actual
  const indexOfLastRow = currentPage * rowsPerPage;
  const indexOfFirstRow = indexOfLastRow - rowsPerPage;
  const currentHospitals = hospitales.slice(indexOfFirstRow, indexOfLastRow);

  // Cambiar de página
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const renderHospitals = () => {
    return (
      <div style={{ marginTop: "20px" }}>
        <h2>Hospitales Registrados</h2>
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
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {currentHospitals.map((hospital, index) => (
                  <tr key={index}>
                    <td>{hospital.id}</td>
                    <td>{hospital.name}</td>
                    <td>{hospital.address}</td>
                    <td>{hospital.phone}</td>
                    <td>
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
    <Suspense fallback="Cargando Traducciones">
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <NavigationBar />
        <h1>Gestión de Hospitales</h1>

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
      <Footer />
    </Suspense>
  );
};

export default ManagementHospital;

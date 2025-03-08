import React, { useEffect, useState, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import CryptoJS from "crypto-js";
import { NavigationBar, Footer } from '../../components';
import { useTranslation } from "react-i18next";

//Apis
import { getListHospital, updateHospital, deleteHospital, addHospital } from "../../api/admin/hospital.api";

/**
 * Componente para la gestión de hospitales.
 * Permite agregar, editar y eliminar hospitales.
 */
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
  const { t: translate } = useTranslation(); // Lista de Hospitales

  const ENCRYPTION_KEY = "my-secure-key";

  useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      navigate("/login");
    } else {
      getList();
    }
  }, []);

  /**
   * Maneja los cambios en el formulario.
   * @param {Object} e - Evento de cambio.
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  /**
   * Maneja el envío del formulario.
   * @param {Object} e - Evento de envío.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convertir los datos en JSON y encriptarlos
    const jsonData = JSON.stringify(formData);
    const encryptedData = CryptoJS.AES.encrypt(jsonData, ENCRYPTION_KEY).toString();

    try {
      // Editando un Hospital
      if (isEditing) {
        const response = await updateHospital(currentHospitalId, formData); // Llamado a la API

        if (response?.status === 200) {
          alert(response?.data?.message);
          setIsEditing(false);

        } else {
          alert(translate("errorupdate"));
        }
      } else {
        // Agregando un nuevo Hospital
        const response = await addHospital(jsonData);
        if (response?.status === 200) {
          alert(response?.data?.message)
          setHospital((prev) => [
            ...prev,
            {
              ...JSON.parse(CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY).toString(CryptoJS.enc.Utf8)),
              id: prev.length,
            },
          ]);
        } else {
          alert(translate("errorregister"));
        }
      }
    } catch (error) {
      const message = error.response.data.message ?? translate("errorupdate");
      if (isEditing) {
        console.error("Error al actualizar el Hospital:", error);
        alert(message);
      } else {
        console.error("Error al crear el Hospital:", error);
        alert(message);
      }
    }
    // Ocultar el formulario
    setShowForm(false);

    // Limpiar el formulario y ocultar el formulario
    cleanFormData();

    // Actualizar la lista de doctores después de agregar/editar
    getList();
  };

  /**
   * Limpia el formulario.
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
   * Maneja la eliminación de un hospital.
   * @param {number} id - ID del hospital a eliminar.
   */
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

  /**
   * Maneja la edición de un hospital.
   * @param {number} id - ID del hospital a editar.
   */
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

  /**
   * Maneja la adición de un nuevo hospital.
   */
  const handleAddNewHospital = () => {
    cleanFormData();
    setIsEditing(false);
    setShowForm(true);
  };

  /**
   * Muestra todos los hospitales registrados.
   * @returns {JSX.Element} - Tabla con la lista de hospitales.
   */
  const renderHospitals = () => {
    return (
      <div style={{ marginTop: "20px" }}>
        <h2>Hopitales Registrados</h2>
        {hospitales.length === 0 ? (
          <p>No hay Hospitales registrados.</p>
        ) : (
          <table border="1" style={{ width: "100%", textAlign: "left" }}>
            <thead>
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Dirección</th>
                <th>Telefono</th>
              </tr>
            </thead>
            <tbody>
              {hospitales.map((hospital, index) => (
                <tr key={index}>
                  <td>{hospital.id}</td>
                  <td>{hospital.name}</td>
                  <td>{hospital.address}</td>
                  <td>{hospital.phone}</td>
                  <td>
                    <button onClick={() => handleEdit(hospital.id)} style={{ marginRight: "10px" }}>
                      Editar
                    </button>
                    <button onClick={() => handleDelete(hospital.id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  };

  /**
   * Obtiene la lista de hospitales.
   */
  const getList = async () => {
    try {
      const response = await getListHospital();
      console.log(response?.data?.hospitals);
      setHospital(response?.data?.hospitals)

    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  return (
    <Suspense fallback="Cargando Traducciones">
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <NavigationBar />
        <h1>Gestión de Hospitales</h1>

        {/* Botones de acción */}
        <div style={{ marginBottom: "20px" }}>
          <button onClick={handleAddNewHospital} style={{ marginRight: "10px" }}>
            Agregar Nuevo Hospital
          </button>
          <button onClick={() => setShowForm(false)}>Ver Todos los Hospitales</button>
        </div>

        {/* Formulario */}
        {showForm && (
          <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "0 auto" }}>
            <h2>{isEditing ? "Editar Hospital" : "Registrar Nuevo Hospital"}</h2>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("name")}</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("address")}</label>
              <input type="text" name="address" value={formData.address} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("phone")}</label>
              <input type="text" name="phone" value={formData.phone} onChange={handleChange} required />
            </div>

            <button type="submit">{isEditing ? "Actualizar" : "Registrar"}</button>
          </form>
        )}

        {/* Lista de hospitales */}
        {!showForm && renderHospitals()}
        <Footer></Footer>
      </div>
    </Suspense>
  );
};

export default ManagementHospital;

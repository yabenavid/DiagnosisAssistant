import React, { useEffect, useState, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import CryptoJS from "crypto-js"; // Para encriptar los datos
import { NavigationBar, Footer } from '../../components';

import { FaEdit, FaPlus, FaList } from 'react-icons/fa';
import { FcEmptyTrash, FcInfo } from "react-icons/fc";
import '/src/styles/admin/Management.css';

import { useTranslation } from "react-i18next";

//Apis
import { getListDoctor, updateDoctor, deleteDoctor, addDoctor } from "../../api/admin/doctor.api";
import { getListHospital } from "../../api/admin/hospital.api"

import { useAuth } from "../../context/AuthContext";

const DoctorManagement = () => {
  const { auth } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    last_name: "",
    second_last_name: "",
    specialism: "",
    "user": {
      email: "",
      password: ""
    },
    hospital: ""
  });


  const [listDoctors, setDoctors] = useState([]); // Lista de doctores registrados
  const [isEditing, setIsEditing] = useState(false); // Indica si estamos editando
  const [currentDoctorId, setCurrentDoctorId] = useState(null); // Doctor en edición
  const [showForm, setShowForm] = useState(false); // Mostrar/ocultar formulario
  const [hospitals, setHospitals] = useState([]);
  const { t: translate } = useTranslation();


  // Cambiar de página
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  const [currentPage, setCurrentPage] = useState(1); // Página actual
  const rowsPerPage = 10; // Número de filas por página
  const ENCRYPTION_KEY = "my-secure-key";

  useEffect(() => {
    if (localStorage.getItem('access_token') === null) {
      navigate("/login");
    } else {
      getList();
      getHospital();
    }

  }, []);

  // Manejar cambios en el formulario
  const handleChange = (e) => {
    const { name, value } = e.target;

    // Si el campo pertenece a "user", actualizarlo correctamente
    if (name === "email" || name === "password") {
      setFormData((prev) => ({
        ...prev,
        user: {
          ...prev.user, // Mantiene los valores anteriores de `user`
          [name]: value // Actualiza solo `email` o `password`
        }
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value // Actualiza los demás campos del formulario
      }));
    }
  };


  // Manejar el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convertir los datos en JSON y encriptarlos
    const jsonData = JSON.stringify(formData);
    const encryptedData = CryptoJS.AES.encrypt(jsonData, ENCRYPTION_KEY).toString();
    console.log("Data editar: ", jsonData);
    try {
      if (isEditing) {
        // Llamar a la API updateDoctor para actualizar el registro del doctor
        console.log("Data editar: ", jsonData);
        const response = await updateDoctor(currentDoctorId, jsonData, auth.accessToken); // Llamado a la API

        if (response?.status === 200) {
          alert(response?.data?.message);

          // Actualizar la lista de doctores en la UI después de la edición
          setIsEditing(false);
        } else {
          alert(translate("errorupdate"));
        }
      } else {
        // Agregar nuevo doctor (si no está en edición)
        const response = await addDoctor(jsonData, auth.accessToken);
        if (response?.status === 200) {
          alert(response?.data?.message);

          setDoctors((prev) => [
            ...prev,
            {
              ...JSON.parse(CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY).toString(CryptoJS.enc.Utf8)),
              id: prev.length,
            }
          ]);
        } else {
          alert(translate("errorregister"));
        }
      }
    } catch (error) {
      const message = error.response.data.message ?? translate("errorupdate");
      if (isEditing) {
        console.error("Error al actualizar el doctor:", error);
        alert(message);
      } else {
        console.error("Error al crear el doctor:", error);
        alert(message);
      }
    }
    // Ocultar el formulario
    setShowForm(false);

    // Limpiar el formulario y ocultar el formulario
    cleanFormData();

    // Actualizar la lista de doctores después de agregar/editar
    await getList();

  };

  // Limpiar el formulario
  const cleanFormData = () => {
    console.log("Limpiando formulario");
    setFormData({
      id: "",
      name: "",
      last_name: "",
      second_last_name: "",
      specialism: "",
      "user": {
        email: "",
        password: ""
      },
      hospital: ""
    });
  }

  // Manejar la eliminación de un doctor
  const handleDelete = async (id) => {
    const confirmed = window.confirm(translate("deleteregister"));

    if (confirmed) {
      try {
        const response = await deleteDoctor(id, auth.accessToken); // Llamada a la API

        if (response?.status === 200) {
          alert(response?.data?.message);
          getList();
        } else {
          alert(response?.data?.message);
        }
      } catch (error) {
        console.error("Error al eliminar el doctor:", error);
        alert(error.response.data.message);
      }
    }
  };

  //Obtener Lista de doctores
  const getList = async () => {

    try {
      const response = await getListDoctor(auth.accessToken);
      console.log(response?.data?.doctors);
      setDoctors(response?.data?.doctors)

    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  // Obtener Lista de Hospitales
  const getHospital = async () => {
    try {
      const response = await getListHospital(auth.accessToken);
      console.log(response);
      setHospitals(response?.data?.hospitals);

    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  // Manejar la edición de un doctor
  const handleEdit = (id) => {
    const doctor = listDoctors.find((doctor) => doctor.id === id);
    if (doctor) {
      setFormData(doctor);
      getHospital();
      setCurrentDoctorId(id);
      setIsEditing(true);
      setShowForm(true); // Mostrar el formulario para edición
    } else {
      console.error("Doctor no encontrado");
    }
  };

  // Manejar la adición de un nuevo doctor
  const handleAddNewDoctor = () => {
    cleanFormData();
    setIsEditing(false);
    setShowForm(true);
  };

  // Mostrar todos los doctores registrados
  const renderDoctors = () => {
    return (
      <div style={{ marginTop: "20px" }}>
        <h2>Doctores Registrados</h2>

        {listDoctors.length === 0 ? (
          <p>No hay doctores registrados.</p>
        ) : (
          <div className="table-responsive">
            <table border="1" style={{ width: "100%", textAlign: "left" }}>
              <thead>
                <tr>
                  <th>Id</th>
                  <th>Nombre</th>
                  <th>Apellido</th>
                  <th>Segundo Apellido</th>
                  <th>Especialidad</th>
                  <th>Email</th>
                  <th>Hospital</th>
                  <th className="files-column">Acción</th>
                </tr>
              </thead>
              <tbody>
                {listDoctors.map((doctor, index) => (
                  <tr key={index}>
                    <td>{doctor.id}</td>
                    <td>{doctor.name}</td>
                    <td>{doctor.last_name}</td>
                    <td>{doctor.second_last_name}</td>
                    <td>{doctor.specialism}</td>
                    <td>{doctor.user.email}</td>
                    <td>{hospitals.find((h) => h.id === parseInt(doctor.hospital))?.name}</td>
                    <td className="files-column">
                      {/* Botón de editar con tooltip */}
                      <div className="tooltip-container">
                        <button onClick={() => handleEdit(doctor.id)} style={{ marginRight: "10px" }}>
                          <FaEdit />
                        </button>
                        <span className="tooltip-text"><FcInfo /> Editar</span>
                      </div>

                      {/* Botón de eliminar con tooltip */}
                      <div className="tooltip-container">
                        <button onClick={() => handleDelete(doctor.id)}>
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
              {Array.from({ length: Math.ceil(listDoctors.length / rowsPerPage) }, (_, i) => (
                <button
                  key={i}
                  onClick={() => paginate(i + 1)}
                  className={currentPage === i + 1 ? "active" : ""}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  };

  return (
    <Suspense fallback="Cargando Traducciones">
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <NavigationBar />
        <h1>Gestión de Doctores</h1>

        {/* Botones de acción */}
        <div className="action-buttons">
          <button onClick={handleAddNewDoctor} style={{ marginRight: "10px" }}><FaPlus /> Agregar </button>
          <button onClick={() => setShowForm(false)}><FaList /> Ver Todos </button>
        </div>

        {/* Formulario */}
        {showForm && (
          <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "0 auto" }}>
            <h2>{isEditing ? "Editar Doctor" : "Registrar Nuevo Doctor"}</h2>

            <div style={{ marginBottom: "15px" }}>
              <label>
                {translate("name")} <span className="required">*</span>
              </label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>
                {translate("lasname")} <span className="required">*</span>
              </label>
              <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("secondlastname")}</label>
              <input type="text" name="second_last_name" value={formData.second_last_name} onChange={handleChange} />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>
                {translate("specialism")} <span className="required">*</span>
              </label>
              <input type="text" name="specialism" value={formData.specialism} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>
                {translate("email")} <span className="required">*</span>
              </label>
              <input type="email" name="email" value={formData.user.email} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("password")}</label>
              <input type="password" name="password" value={formData.user.password} onChange={handleChange} />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>
                {translate("hospital")} <span className="required">*</span>
              </label>
              <select name="hospital" value={formData.hospital} onChange={handleChange} required>
                <option value="">{translate("selectedhospital")}</option>
                {hospitals.map((hospital) => (
                  <option key={hospital.id} value={hospital.id}>
                    {hospital.name}
                  </option>
                ))}
              </select>
            </div>

            <button type="submit">{isEditing ? "Actualizar" : "Registrar"}</button>
          </form>
        )}

        {/* Lista de doctores */}
        {!showForm && renderDoctors()}
      </div>
      <Footer />
    </Suspense>
  );
};

export default DoctorManagement;

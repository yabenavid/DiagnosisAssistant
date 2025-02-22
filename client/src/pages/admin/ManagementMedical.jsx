import React, { useEffect, useState, Suspense } from "react";
import CryptoJS from "crypto-js"; // Para encriptar los datos
import { NavigationBarAdmin, Footer } from '../../components';

import { useTranslation } from "react-i18next";

//Apis
import { getListDoctor, updateDoctor, deleteDoctor, addDoctor } from "../../api/admin/doctor.api";
import { getListHospital } from "../../api/admin/hospital.api"

const DoctorManagement = () => {

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    last_name: "",
    second_last_name: "",
    specialism: "",
    "credential":{
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

  useEffect(() => {
    getList(); 
    getHospital(); 
  }, []);

  // const hospitals = [
  //   { id: 1, name: "Hospital General" },
  //   { id: 2, name: "Hospital Clínico" },
  //   { id: 3, name: "Hospital Central" },
  // ];

  const ENCRYPTION_KEY = "my-secure-key";

  // Manejar cambios en el formulario
  // const handleChange = (e) => {
  //   const { name, value } = e.target;
  //   setFormData({ ...formData, [name]: value });
  // };
  const handleChange = (e) => {
    const { name, value } = e.target;

    // Si el campo pertenece a "credential", actualizarlo correctamente
    if (name === "email" || name === "password") {
        setFormData((prev) => ({
            ...prev,
            credential: {
                ...prev.credential, // Mantiene los valores anteriores de `credential`
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
    console.log(jsonData);
    if (isEditing) {
      // Llamar a la API updateDoctor para actualizar el registro del doctor
      try {
        console.log(currentDoctorId);
        const response = await updateDoctor(currentDoctorId, jsonData); // Llamado a la API

        if (response?.status === 200) {
          alert(response?.data?.message);

          // Actualizar la lista de doctores en la UI después de la edición
          // setDoctors((prev) =>
          //     prev.map((doctor) =>
          //         doctor.id === currentDoctorId ? { ...formData, id: currentDoctorId } : doctor
          //     )
          // );
          setIsEditing(false);
          setShowForm(false);
        } else {
          alert(translate("errorupdate"));
        }
      } catch (error) {
        console.error("Error al actualizar el doctor:", error);
        alert(translate("alertupdated"));
      }
    } else {
      // Agregar nuevo doctor (si no está en edición)
      try {

        console.log(jsonData);
        const response = await addDoctor(jsonData);
        if (response?.status === 200) {
          alert(response?.data?.message)

          setDoctors((prev) => [
            ...prev,
            {
              ...JSON.parse(CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY).toString(CryptoJS.enc.Utf8)),
              id: prev.length,
            },
          ]);
        } else {
          alert(translate("errorregister"));
        }
      } catch (error) {
        console.error("Error al crear el doctor:", error);
        alert(translate("errorregister"));
      }
    }

    // Limpiar el formulario
    setFormData({
      id: "",
      name: "",
      last_name: "",
      second_last_name: "",
      specialism: "",
      "credential":{
        email: "",
        password: ""
      },
      hospital: ""
    });

    setShowForm(false); // Ocultar el formulario
  };


  // Manejar la eliminación de un doctor
  const handleDelete = async (id) => {
    const confirmed = window.confirm(translate("deleteregister"));

    if (confirmed) {
      try {
        const response = await deleteDoctor(id); // Llamada a la API

        if (response?.status === 200) {
          alert(response?.data?.message);

          // Actualizar la lista de doctores después de eliminar
          //setDoctors((prev) => prev.filter((doctor) => doctor.id !== id));
        } else {
          alert(response?.data?.message);
        }
      } catch (error) {
        console.error("Error al eliminar el doctor:", error);
        alert(translate("errordeleted"));
      }
    }
  };

  //Obtener Lista de doctores
  const getList = async () => {

    try{
      const response = await getListDoctor();
      console.log(response?.data?.doctors);
      setDoctors(response?.data?.doctors)

    }catch(error){
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  // Obtener Lista de Hospitales
  const getHospital = async () => {
    try {
      const response = await getListHospital();
      console.log(response);
      setHospitals(response?.data?.hospitals);

    } catch (error) {
      console.error("Error al cargar la lista Hospitales:", error);
      alert("Error al obtener los Hospitales, por favor intente de nuevo.");
    }
  };

  // Manejar la edición de un doctor
  const handleEdit = (id) => {
    const doctor = listDoctors[id];
    setFormData(doctor);
    getHospital();
    setCurrentDoctorId(id);
    setIsEditing(true);
    setShowForm(true); // Mostrar el formulario para edición
  };

  // Mostrar todos los doctores registrados
  const renderDoctors = () => {
    return (
      <div style={{ marginTop: "20px" }}>
        <h2>Doctores Registrados</h2>

        {listDoctors.length === 0 ? (
          <p>No hay doctores registrados.</p>
        ) : (
          <table border="1" style={{ width: "100%", textAlign: "left" }}>
            <thead>
              <tr>
                <th>#</th>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Segundo Apellido</th>
                <th>Especialidad</th>
                <th>Email</th>
                <th>Hospital</th>
                <th>Acciones</th>
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
                  <td>{doctor.credential.email}</td>
                  <td>{hospitals.find((h) => h.id === parseInt(doctor.hospital))?.name}</td>
                  <td>
                    <button onClick={() => handleEdit(doctor.id)} style={{ marginRight: "10px" }}>
                      Editar
                    </button>
                    <button onClick={() => handleDelete(doctor.id)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  };

  
  return (
    <Suspense fallback="Cargando Traducciones">
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <NavigationBarAdmin></NavigationBarAdmin>
        <h1>Gestión de Doctores</h1>

        {/* Botones de acción */}
        <div style={{ marginBottom: "20px" }}>
          <button onClick={() => setShowForm(true)} style={{ marginRight: "10px" }}>
            Agregar Nuevo Doctor
          </button>
          <button onClick={() => setShowForm(false)}>Ver Todos los Doctores</button>
        </div>

        {/* Formulario */}
        {showForm && (
          <form onSubmit={handleSubmit} style={{ maxWidth: "400px", margin: "0 auto" }}>
            <h2>{isEditing ? "Editar Doctor" : "Registrar Nuevo Doctor"}</h2>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("name")}</label>
              <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("lasname")}</label>
              <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("secondlastname")}</label>
              <input type="text" name="second_last_name" value={formData.second_last_name} onChange={handleChange} />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("specialism")}</label>
              <input type="text" name="specialism" value={formData.specialism} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("email")}</label>
              <input type="email" name="email" value={formData.credential.email} onChange={handleChange} required />
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("password")}</label>
              <input type="password" name="password" value={formData.credential.password} onChange={handleChange}/>
            </div>

            <div style={{ marginBottom: "15px" }}>
              <label>{translate("hospital")}</label>
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
        <Footer></Footer>
      </div>
    </Suspense>
  );
};

export default DoctorManagement;

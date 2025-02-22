import axios from 'axios'
const doctorApi = axios.create({
    //baseURL: 'https://diagnostico.free.beeceptor.com/'
    baseURL: 'https://7bc9b5a9-ac63-4468-87cc-13e8f48b27d6.mock.pstmn.io/'
})

// export const getListDoctor = () => doctorApi.get("/");

export const sendImages = (doctorId, updatedData) => doctorApi.put("/" + doctorId, updatedData);

// export const deleteDoctor = (doctorId) => doctorApi.delete("/" + doctorId);

// export const addDoctor = (data) => doctorApi.post("/",data);

// TODO: Enviar en el encabezado de la peticion el bearer token 

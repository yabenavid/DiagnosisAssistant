import axios from 'axios'
import { getAuthHeaders, getAuthHeadersJson } from '../../hooks/Authorization';

const doctorApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/doctors',
    ...getAuthHeadersJson()
})

export const getListDoctor = () => doctorApi.get("/");

export const updateDoctor = (doctorId, updatedData) => doctorApi.put("/" + doctorId, updatedData);

export const deleteDoctor = (doctorId) => doctorApi.delete("/" + doctorId);

export const addDoctor = (data) => doctorApi.post("/",data);

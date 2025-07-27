import axios from 'axios'
import { getAuthHeaders, getAuthHeadersJson } from '../../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/doctors'
    : 'http://127.0.0.1:8000/api/v1/doctors';

const doctorApi = (token) => axios.create({
    baseURL: API_BASE_URL,
    ...getAuthHeadersJson(token)
})

export const getListDoctor = (token) => doctorApi(token).get("/");

export const updateDoctor = (doctorId, updatedData, token) => doctorApi(token).put("/" + doctorId, updatedData);

export const deleteDoctor = (doctorId, token) => doctorApi(token).delete("/" + doctorId);

export const addDoctor = (data, token) => doctorApi(token).post("/",data);

import axios from 'axios'
import { getAuthHeaders, getAuthHeadersJson } from '../../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/hospitals'
    : 'http://127.0.0.1:8000/api/v1/hospitals';

const hospitalApi = (token) => axios.create({
     baseURL: API_BASE_URL,
     ...getAuthHeadersJson(token)
})

export const getListHospital = (token) => hospitalApi(token).get("/");

export const updateHospital = (hospitalId, updatedData, token) => hospitalApi(token).put("/" + hospitalId, updatedData);

export const deleteHospital = (hospitalId, token) => hospitalApi(token).delete("/" + hospitalId);

export const addHospital = (data, token) => hospitalApi(token).post("/",data);

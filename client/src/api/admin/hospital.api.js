import axios from 'axios'
import { getAuthHeaders, getAuthHeadersJson } from '../../hooks/Authorization';

const hospitalApi = axios.create({
     baseURL: 'http://127.0.0.1:8000/api/v1/hospitals',
     ...getAuthHeadersJson()
})

export const getListHospital = () => hospitalApi.get("/");

export const updateHospital = (hospitalId, updatedData) => hospitalApi.put("/" + hospitalId, updatedData);

export const deleteHospital = (hospitalId) => hospitalApi.delete("/" + hospitalId);

export const addHospital = (data) => hospitalApi.post("/",data);

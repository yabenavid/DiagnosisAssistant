import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';

const dataSetApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/datasets/images/',
    ...getAuthHeaders()
});

const dataSetCount = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/datasets/count/',
    ...getAuthHeaders()
});

export const addDataSet = (data) => dataSetApi.post("/", data);

export const getCountDataSet = () => dataSetCount.get("/");

import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';

const dataSetApi = (token) => axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/datasets/images/',
    ...getAuthHeaders(token)
});

const dataSetCount = (token) => axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/datasets/count/',
    ...getAuthHeaders(token)
});

export const addDataSet = (data, token) => dataSetApi(token).post("/", data);

export const getCountDataSet = (token) => dataSetCount(token).get("/");

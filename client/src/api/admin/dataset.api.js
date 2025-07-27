import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';

const API_DATESET_BASE_URL = import.meta.env.PROD
    ? '/api/v1/datasets/images'
    : 'http://127.0.0.1:8000/api/v1/datasets/images';

 const API_COUNT_BASE_URL = import.meta.env.PROD
    ? '/api/v1/datasets/count'
    : 'http://127.0.0.1:8000/api/v1/datasets/count';
   
const dataSetApi = (token) => axios.create({
    baseURL: API_DATESET_BASE_URL,
    ...getAuthHeaders(token)
});

const dataSetCount = (token) => axios.create({
    baseURL: API_COUNT_BASE_URL,
    ...getAuthHeaders(token)
});

export const addDataSet = (data, token) => dataSetApi(token).post("/", data);

export const getCountDataSet = (token) => dataSetCount(token).get("/");

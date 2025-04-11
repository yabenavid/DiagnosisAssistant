import axios from 'axios'
import { getAuthHeadersJson } from '../../hooks/Authorization';

const historyApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/history',
    ...getAuthHeadersJson()
})

export const getHistory = () => historyApi.get("/");

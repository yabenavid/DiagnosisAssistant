import axios from 'axios'
import { getAuthHeadersJson } from '../../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/history'
    : 'http://127.0.0.1:8000/api/v1/history';

const historyApi = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json"
    },
    withCredentials: true
})

export const getHistory = (token) => {
    return historyApi.get("/", {
        headers: {
            "Authorization": `Bearer ${token}` // Configura el token dinámicamente
        }
    });
};

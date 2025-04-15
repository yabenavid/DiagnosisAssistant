import axios from 'axios'
import { getAuthHeadersJson } from '../../hooks/Authorization';

const historyApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/history',
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

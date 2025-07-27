import axios from 'axios'
import { getAuthHeadersJson } from '../../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/history'
    : 'http://127.0.0.1:8000/api/v1/history';

const sendApi = (token) => axios.create({
    baseURL: API_BASE_URL,
    ...getAuthHeadersJson(token)
})

export const sendEmail = (historyId, data, token) => sendApi(token).post("/" + historyId + "/send/", data);

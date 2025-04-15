import axios from 'axios'
import { getAuthHeadersJson } from '../../hooks/Authorization';

const sendApi = (token) => axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/history',
    ...getAuthHeadersJson(token)
})

export const sendEmail = (historyId, data, token) => sendApi(token).post("/" + historyId + "/send/", data);

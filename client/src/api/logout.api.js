import axios from 'axios';
import { getAuthHeadersJson } from '../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/logout'
    : 'http://127.0.0.1:8000/logout';

const loginApi = (token) => axios.create({
    baseURL: API_BASE_URL,
    ...getAuthHeadersJson(token)
});

export const LogoutUser = (refresh, token) => loginApi(token).post('/',refresh);

import axios from 'axios';
import { getAuthHeadersJson } from '../hooks/Authorization';

const loginApi = (token) => axios.create({
    baseURL: 'http://127.0.0.1:8000/logout/',
    ...getAuthHeadersJson(token)
});

export const LogoutUser = (refresh, token) => loginApi(token).post('/',refresh);

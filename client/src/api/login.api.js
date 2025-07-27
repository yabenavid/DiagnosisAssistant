import axios from 'axios'

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/token'
    : 'http://127.0.0.1:8000/token';

const loginApi= axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
})


export const ValidationUser = (infouser) => loginApi.post('/',infouser);

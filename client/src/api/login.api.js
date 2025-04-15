import axios from 'axios'

const loginApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/token',
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
})


export const ValidationUser = (infouser) => loginApi.post('/',infouser);

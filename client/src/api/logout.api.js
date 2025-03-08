import axios from 'axios'

const loginApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/logout/',
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem('access_token')
    },
    withCredentials: true
})

export const LogoutUser = (refresh) => loginApi.post('/',refresh);

import axios from 'axios'

const loginApi = axios.create({
    // baseURL: 'https://7bc9b5a9-ac63-4468-87cc-13e8f48b27d6.mock.pstmn.io',
    baseURL: 'http://127.0.0.1:8000/logout/',
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
})

export const LogoutUser = (refresh) => loginApi.post('/',refresh);
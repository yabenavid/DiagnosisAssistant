import axios from 'axios'

const sendDiagnosticApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/send-diagnostic',
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
})


export const EmailsDiagnostic = (data) => sendDiagnosticApi.post('/',data); 
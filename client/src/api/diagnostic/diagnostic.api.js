import axios from 'axios'

const segmentApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/segment-image',
    headers: {
        "Content-Type": "multipart/form-data"
    },
    withCredentials: true
})


export const SegmentImages = (data) => segmentApi.post('/',data); 


import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';


const segmentApi = (token) => axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/evaluate-images',
    ...getAuthHeaders(token)
})


export const SegmentImages = (data, token) => segmentApi(token).post('/',data); 


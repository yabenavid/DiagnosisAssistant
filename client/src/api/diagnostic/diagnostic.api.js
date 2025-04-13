import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';


const segmentApi = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/evaluate-images',
    ...getAuthHeaders()
})


export const SegmentImages = (data) => segmentApi.post('/',data); 


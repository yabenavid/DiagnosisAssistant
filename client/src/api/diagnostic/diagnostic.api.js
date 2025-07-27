import axios from 'axios';
import { getAuthHeaders } from '../../hooks/Authorization';

const API_BASE_URL = import.meta.env.PROD
    ? '/api/v1/evaluate-images'
    : 'http://127.0.0.1:8000/api/v1/evaluate-images';

const segmentApi = (token) => axios.create({
    baseURL: API_BASE_URL,
    ...getAuthHeaders(token)
})

export const SegmentImages = (data, token) => segmentApi(token).post('/',data); 

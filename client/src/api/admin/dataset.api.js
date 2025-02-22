import axios from 'axios';

const dataSetApi = axios.create({
    //baseURL: 'https://diagnostico.free.beeceptor.com/dataset',
    baseURL: 'https://7bc9b5a9-ac63-4468-87cc-13e8f48b27d6.mock.pstmn.io/dataset/',
    headers: {
        "Content-Type": "multipart/form-data"
    }
});

export const addDataSet = (data) => dataSetApi.post("/", data);

export const getCountDataSet = () => dataSetApi.get("/");
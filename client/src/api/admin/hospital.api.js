import axios from 'axios'
const hospitalApi = axios.create({
    //baseURL: 'https://diagnostico.free.beeceptor.com/hospital'
    baseURL: 'https://7bc9b5a9-ac63-4468-87cc-13e8f48b27d6.mock.pstmn.io/hospital/'
})

export const getListHospital = () => hospitalApi.get("/");

export const updateHospital = (hospitalId, updatedData) => hospitalApi.put("/" + hospitalId, updatedData);

export const deleteHospital = (hospitalId) => hospitalApi.delete("/" + hospitalId);

export const addHospital = (data) => hospitalApi.post("/",data);

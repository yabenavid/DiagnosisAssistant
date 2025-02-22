import axios from 'axios'

const loginApi = axios.create({
    baseURL: 'https://7bc9b5a9-ac63-4468-87cc-13e8f48b27d6.mock.pstmn.io'
})

export const ValidationUser = (infouser) => loginApi.post('/',infouser);


export const getAuthHeaders = () => ({
    headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer " + localStorage.getItem('access_token')
    },
    withCredentials: true
});

export const getAuthHeadersJson = (token) => ({
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    },
    withCredentials: true
});

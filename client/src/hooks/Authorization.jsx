export const getAuthHeaders = () => ({
    headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer " + localStorage.getItem('access_token')
    },
    withCredentials: true
});

export const getAuthHeadersJson = () => ({
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem('access_token')
    },
    withCredentials: true
});

export const getAuthHeaders = (token) => ({
    headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer " + token
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

import axios from 'axios';
const apiUrl = "http://127.0.0.1:8000/api";
export const requestHeaders = {
    "Content-Type": "application/json",
    "Authorization": '',
};
export const multipartFormData = {
    "Content-Type": "multipart/form-data",
    "Authorization": '',
}
export const noTokenRequest = axios.create({
    baseURL:apiUrl,
    headers:{"Content-Type":"application/json"}
})
export const withTokenRequest = axios.create({
    baseURL:apiUrl,
})
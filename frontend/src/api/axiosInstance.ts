import axios from "axios";

const USER_API_URL = "http://localhost:8000/api/users";
const SERVICE_API_URL = "http://localhost:8000/v1/dub"

const axiosUserInstance = axios.create({
  baseURL: USER_API_URL,
  withCredentials: true, // 쿠키 자동 포함
});

const axiosServiceInstance = axios.create({
  baseURL: SERVICE_API_URL,
  withCredentials: true, // 쿠키 자동 포함
});

export {axiosUserInstance, axiosServiceInstance};

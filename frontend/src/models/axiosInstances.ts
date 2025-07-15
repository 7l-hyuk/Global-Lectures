import axios from "axios";


const axiosAuthInstance = axios.create(
    {
        baseURL: process.env.REACT_APP_AUTH_API_URL,
        withCredentials: true
    }
);


const axiosDubbingInstance = axios.create(
    {
        baseURL: process.env.REACT_APP_DUBBING_API_URL,
        withCredentials: true
    }
);


const axiosVideoInstance = axios.create(
    {
        baseURL: process.env.REACT_APP_VIDEO_API_URL,
        withCredentials: true
    }
);


export {axiosAuthInstance, axiosDubbingInstance, axiosVideoInstance};
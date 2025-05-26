import {axiosServiceInstance} from "./axiosInstance";

interface DubData {
    video: File;
    sourceLang: string;
    targetLang: string;
} 

export const dub = async (dubData: DubData) => {
  try {
    const res = await axiosServiceInstance.post("", dubData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
    console.log(res.data)
    return res
  } catch (error) {
    console.error("upload faild", error)
  }
};

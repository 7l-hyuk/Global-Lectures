import {axiosServiceInstance} from "./axiosInstance";
import { SubtitleEntry } from "./video";


interface DubData {
    video: File;
    sourceLang: string;
    targetLang: string;
} 

interface DubAudioData {
  videoId: number,
  subtitle: SubtitleEntry[],
  audioPresignedUrl: string,
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


export const dubByAudio = async (dubData: DubAudioData) => {
  try {
    const res = await axiosServiceInstance.post("/audio", dubData);
    console.log(res.data);
    return res;
  } catch (error) {
    console.error("upload faild", error);
  }
}
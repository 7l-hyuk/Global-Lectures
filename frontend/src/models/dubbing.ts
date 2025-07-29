import { axiosDubbingInstance } from "./axiosInstances";
import { DubbingRequest } from "../types/dubbing";


enum ContentType {
  JSON = "application/json",
  FORM = "application/x-www-form-urlencoded",
  MULTIPART = "multipart/form-data",
}


export const dubbingVideo = async (dubbingRequest: DubbingRequest) => {
    return await axiosDubbingInstance.post(
        "",
        dubbingRequest,
        {
            headers: {"Content-Type": ContentType.MULTIPART}
        }
    );
};

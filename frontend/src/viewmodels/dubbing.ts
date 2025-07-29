import { dubbingVideo as dubbingAPI } from "../models/dubbing";
import { DubbingRequest } from "../types/dubbing";
import { LanguageType, LangCode } from "../types/components";

export const dubbingVideo = async (dubbingRequest: DubbingRequest) => {
    try {
        await dubbingAPI(dubbingRequest)
    } catch (err) {
        console.error(err)
    }
};

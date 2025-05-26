import {axiosUserInstance} from "./axiosInstance";

interface LoginData {
  username: string;
  password: string;
}

interface SignupData {
  username: string;
  email: string;
  password: string;
}

// 회원가입
export const signup = async (data: SignupData) => {
  return await axiosUserInstance.post("/signup", data);
};

// 로그인
export const login = async (data: LoginData) => {
  return await axiosUserInstance.post("/login", data);
};

// 내 정보 불러오기
export const fetchMe = async () => {
  return await axiosUserInstance.get("/me");
};

// 로그아웃
export const logout = async () => {
  return await axiosUserInstance.post("/logout", {});
};

export interface UserSignup {
  username: string;
  email: string;
  password: string;
}


export interface UserSignin {
  username: string;
  password: string;
}


export interface User {
  username: string;
}


export interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  fetchCurrentUser: () => Promise<void>;
  userSignout: () => Promise<void>;
}

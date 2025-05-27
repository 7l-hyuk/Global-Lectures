export interface User {
  username: string;
}

export interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  fetchCurrentUser: () => Promise<void>;
  logout: () => Promise<void>;
}
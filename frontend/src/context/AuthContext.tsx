import { createContext, useContext, useState, useEffect } from "react";
import { fetchMe, logout as logoutAPI } from "../api/auth";

interface User {
  username: string;
}

interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  fetchCurrentUser: () => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const fetchCurrentUser = async () => {
    try {
      const res = await fetchMe();
      setUser({ username: res.data.username });
    } catch {
      setUser(null);
    }
  };

  const logout = async () => {
    try {
        await logoutAPI();
        setUser(null);
    } catch (err) {
        console.error("logout fail", err)
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, fetchCurrentUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

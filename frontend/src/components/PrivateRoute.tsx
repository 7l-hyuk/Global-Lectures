import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) return null;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
};


export default PrivateRoute;
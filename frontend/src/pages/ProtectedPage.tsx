import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";


const ProtectedPage: React.FC = () => {
  const {user} = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div>
      <h1>보호된 페이지</h1>
      <p>안녕하세요, {user.username}님. 이 페이지는 로그인한 사람만 볼 수 있어요.</p>
    </div>
  );
};

export default ProtectedPage;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { faUser, faLock, faSignIn } from "@fortawesome/free-solid-svg-icons";

import { login } from "../api/auth";
import { useAuth } from "../context/AuthContext";
import styles from "../css/Login.module.css"
import { BaseButton, LoginInput } from "../components/Form";


const Login: React.FC = () => {
  const {fetchCurrentUser} = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      await login({username, password})
      await fetchCurrentUser();
      navigate("/");
    } catch (err) {
      alert("로그인 실패");
    }
  };

  return (
    <div className={styles.LoginFormContainer}>
      <h1>LOGIN</h1>
      <LoginInput
        label="E-Mail Address or Username"
        value={username}
        type="text"
        onChange={setUsername}
        styles={styles}
        icon={faUser}
      />
      <LoginInput
        label="Password"
        value={password}
        type="password"
        onChange={setPassword}
        styles={styles}
        icon={faLock}
      />
      <div className={styles.LoginButtonContainer}>
          <BaseButton label="Login" icon={faSignIn} buttonStyle={styles.LoginButton} onClick={handleLogin} disabled={false} />
      </div>
    </div>
  );
};

export default Login;

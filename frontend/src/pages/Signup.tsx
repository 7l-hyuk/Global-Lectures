import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { faUser } from "@fortawesome/free-solid-svg-icons";

import { signup } from "../api/auth";
import styles from "../css/Signup.module.css"
import { BaseButton } from "../components/Form";
import { SignupInput } from "../components/Form";


const Signup: React.FC = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await signup({username, email, password});
      alert("회원가입 성공! 로그인 해주세요.");
      navigate("/login");
    } catch (err) {
      alert("회원가입 실패");
    }
  };

  return (
    <div className={styles.SignupFormContainer}>
      <h1>Register</h1>
      <div>
        <SignupInput 
          label="Choose Username"
          type="text"
          description="Only letters, numbers, - and _ can be used." 
          value={username} 
          onChange={setUsername}
          styles={styles}
        />
        <SignupInput 
          label="Email Address"
          type="text"
          description="Not used for marketing. We'll never share your email with anyone else." 
          value={email} 
          onChange={setEmail} 
          styles={styles}
        />
        <SignupInput 
          label="Password"
          type="password"
          description="At least 8 characters." 
          value={password} 
          onChange={setPassword}
          styles={styles}
        />
        <div className={styles.RegisterButtonContainer}>
          <BaseButton label="Register" icon={faUser} buttonStyle={styles.RegisterButton} onClick={handleSignup} disabled={false} />
        </div>
      </div>
    </div>
  );
};

export default Signup;

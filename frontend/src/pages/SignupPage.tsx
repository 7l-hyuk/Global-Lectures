import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import { userSignup as signupAPI } from "../models/auth";
import { SignupFormGroupProps } from "../types/components";
import { IconButton } from "../components/Button";
import styles from "../styles/SignupPage.module.css";


const SignupFormGroup: React.FC<SignupFormGroupProps> = ({ label, type, value, description, setValue }) => {
  const [showPassword, setShowPassword] = useState(false);

  const isPassword = type === "password";
  const inputType = isPassword && !showPassword ? "password" : "text";
  const toggleIcon = showPassword ? faEye : faEyeSlash;

  return (
    <div className={styles.SignupFormGroupContainer}>
      <label>{label}</label>
      <div className={styles.SignupFormGroupInputContainer}>
        <div className={styles.SignupFormGroupInput}>
            <input
            value={value}
            type={inputType}
            onChange={(event) => setValue(event.target.value)}
            />
            {isPassword && (
            <button
                type="button"
                onClick={() => setShowPassword((prev) => !prev)}
            >
                <FontAwesomeIcon icon={toggleIcon} />
            </button>
            )}
        </div>
        <small>{description}</small>
      </div>
    </div>
  )
}

const SignupPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const userSignup = async () => {
    try {
      await signupAPI({ username, email, password });
      alert("Registration success");
      navigate("/signin");
    } catch (err) {
      alert("Registration fail");
    }
  };

  return (
    <div className={styles.SignupFormContent}>
      <h1>REGISTER</h1>
      <SignupFormGroup
        label="Choose Username"
        description="Only letters, numbers, - and _ can be used."
        value={username}
        type="text"
        setValue={setUsername}
      />
      <SignupFormGroup
        label="Email Address"
        description="Not used for marketing. We'll never share your email with anyone else."
        value={email}
        type="text"
        setValue={setEmail}
      />
      <SignupFormGroup
        label="Password"
        description="At least 8 characters."
        value={password}
        type="password"
        setValue={setPassword}
      />
      <div className={styles.SignupFormAction}>
      <IconButton
        icon={faUser}
        label="Register"
        color="red"
        buttonType="Button"
        onClick={userSignup}
      />
      </div>
    </div>
  );
};


export default SignupPage;
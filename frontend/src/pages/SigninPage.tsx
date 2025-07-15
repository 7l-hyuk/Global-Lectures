import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faLock, faSignIn } from "@fortawesome/free-solid-svg-icons";

import { useAuth } from "../viewmodels/AuthContext";
import { userSignin as signinAPI } from "../models/auth";
import { SigninFormGroupProps } from "../types/components";
import Button from "../components/Button";
import styles from "../styles/SigninPage.module.css";


const SigninFormGroup: React.FC<SigninFormGroupProps> = 
  ({ icon, label, type, value, setValue }) => {
  return (
    <div className={styles.SigninFormGroupContainer}>
      <label>{label}</label>
      <div>
        <FontAwesomeIcon icon={icon} />
        <input
          value={value}
          type={type}
          onChange={(event) => setValue(event.target.value)}
        />
      </div>
    </div>
  )
}

const SigninPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { fetchCurrentUser } = useAuth()
  const navigate = useNavigate();

  const userSignin = async () => {
    try {
      await signinAPI({ username, password });
      await fetchCurrentUser();
      navigate("/");
    } catch (err) {
      alert("Invalid username or password");
    }
  };

  return (
    <div className={styles.SigninFormContainer}>
      <div className={styles.SigninFormContent}>
        <h1>SIGN IN</h1>
        <SigninFormGroup
          icon={faUser}
          label="E-Mail Address or Username"
          value={username}
          type="text"
          setValue={setUsername}
        />
        <SigninFormGroup
          icon={faLock}
          label="Password"
          value={password}
          type="password"
          setValue={setPassword}
        />
        <div className={styles.SiginFormAction}>
        <Button
          icon={faSignIn}
          label="Sign In"
          color="red"
          onClick={userSignin}
        />
        </div>
      </div>
    </div>
  );
};


export default SigninPage;
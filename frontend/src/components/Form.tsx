import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { ButtonProps, InputProps, LoginInputProps } from "./props";

const BaseButton: React.FC<ButtonProps> = ({label, icon, onClick, buttonStyle, disabled}) => {
  return (
    <button className={buttonStyle} onClick={onClick} disabled={disabled}>
        <FontAwesomeIcon icon={icon} style={{marginRight: "1rem"}}/>
        {label}
    </button>
  );
}


const SignupInput: React.FC<InputProps> = ({label, type, description, value, onChange, styles}) => {
  return (
    <div className={styles.row}>
      <label className={styles.Label}>{label}</label>
      <div className={styles.InputContainer}>
        <input
          className={styles.Input}
          value={value}
          type={type}
          onChange={(e) => onChange(e.target.value)} 
        />
        <small className={styles.Description}>{description}</small>
      </div>
    </div>
  );
}

const LoginInput: React.FC<LoginInputProps> = ({label, type, value, onChange, styles, icon}) => {
  return (
    <div className={styles.row}>
    <div>
        <FontAwesomeIcon icon={icon}/>
    </div> 
      <label className={styles.Label}>{label}</label>
      <div className={styles.InputContainer}>
        <input
          className={styles.Input}
          value={value}
          type={type}
          onChange={(e) => onChange(e.target.value)} 
        />
      </div>
    </div>
  );
}



export {BaseButton, SignupInput, LoginInput};
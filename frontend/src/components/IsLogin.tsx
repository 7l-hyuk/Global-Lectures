import React from "react"
import { useAuth } from "../context/AuthContext"
import styles from "../css/Navbar.module.css"
import { Dropdown } from "./Dropdown"


const IsLogin: React.FC = () => {
  const { user } = useAuth();
  return (
    <>
      {user ? (
        <Dropdown />
      ) : (
        <div className={styles.navbarLinks}>
          <a href="http://localhost:3000/signup">Sign Up</a>
          <a href="http://localhost:3000/login">Log In</a>
        </div>
      )}
    </>
  );
}


export {IsLogin};


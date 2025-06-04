import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDatabase, faUser, faCartShopping } from "@fortawesome/free-solid-svg-icons";
import { Outlet } from "react-router-dom";
import styles from "../css/VideoStack.module.css";


const UserPageLayout: React.FC = () => {
  return (
    <div className={styles.UserPageLayout}>
      <ul className={styles.UserPageMenu}>
        <li className={styles.MenuHeader}>
          <span>YOUR ACCOUNT</span>
        </li>
        <li className={styles.MenuItem}>
          <FontAwesomeIcon icon={faDatabase} style={{marginRight: "10px"}}/>
          <a href="/videos" style={{color: "inherit", textDecoration: "none"}}>
            video
          </a>
        </li>
        <li className={styles.MenuItem}>
          <FontAwesomeIcon icon={faUser} style={{marginRight: "10px"}}/>
          <a href="/videos" style={{color: "inherit", textDecoration: "none"}}>
            account
          </a>
        </li>
        <li className={styles.MenuItem}>
          <FontAwesomeIcon icon={faCartShopping} style={{marginRight: "10px"}}/>
          <a href="/videos" style={{color: "inherit", textDecoration: "none"}}>
            billing
          </a>
        </li>
      </ul>
      <Outlet />
    </div>
  );
};

export default UserPageLayout;
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDatabase, faUser, faCartShopping } from "@fortawesome/free-solid-svg-icons";
import { Outlet, useLocation, Link } from "react-router-dom";
import styles from "../css/VideoStack.module.css";

const UserPageLayout: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname.startsWith(path);

  return (
    <div className={styles.UserPageLayout}>
      <ul className={styles.UserPageMenu}>
        <li className={styles.MenuHeader}>
          <span>your account</span>
        </li>
        <li
          className={styles.MenuItem}
          style={isActive("/videos") ? { backgroundColor: "#f5f5f5" } : {}}
        >
          <FontAwesomeIcon icon={faDatabase} style={{ marginRight: "10px" }} />
          <Link to="/videos" style={{ color: "inherit", textDecoration: "none" }}>
            video
          </Link>
        </li>
        <li
          className={styles.MenuItem}
          style={isActive("/account") ? { backgroundColor: "#f5f5f5" } : {}}
        >
          <FontAwesomeIcon icon={faUser} style={{ marginRight: "10px" }} />
          <Link to="/account" style={{ color: "inherit", textDecoration: "none" }}>
            account
          </Link>
        </li>
        <li
          className={styles.MenuItem}
          style={isActive("/billing") ? { backgroundColor: "#f5f5f5" } : {}}
        >
          <FontAwesomeIcon icon={faCartShopping} style={{ marginRight: "10px" }} />
          <Link to="/billing" style={{ color: "inherit", textDecoration: "none" }}>
            billing
          </Link>
        </li>
      </ul>
      <Outlet />
    </div>
  );
};

export default UserPageLayout;

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ButtonProps } from "../types/components";
import styles from "../styles/Button.module.css";

const Button: React.FC<ButtonProps> = ({icon, label, onClick, color = "red"}) => {
    return (
        <button
            className={`${styles.Button} ${styles[color]}`}
            onClick={onClick}
        >
            <FontAwesomeIcon icon={icon} />
            {label}
        </button>
    );
};


export default Button;

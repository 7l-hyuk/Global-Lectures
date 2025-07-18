import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ButtonProps, BasicButtonProps, CountryButtonProps } from "../types/components";
import styles from "../styles/Button.module.css";
// @ts-ignore
import Flag from 'react-world-flags'

const IconButton: React.FC<ButtonProps> = ({icon, label, onClick, color = "red", buttonType = "Button"}) => {
    return (
        <button
            className={`${styles[buttonType]} ${styles[color]}`}
            onClick={onClick}
        >
            {/* <FontAwesomeIcon icon={icon} /> */}
            <Flag code="KR" style={{ width: 24, height: 16 }} />
            {label}
        </button>
    );
};

const ButtonIcon: React.FC<ButtonProps> = ({icon, label, onClick, color = "red", buttonType = "Button"}) => {
    return (
        <button
            className={`${styles[buttonType]} ${styles[color]}`}
            onClick={onClick}
        >
            {label}
            <FontAwesomeIcon icon={icon} />
        </button>
    );
};

const BasicButton: React.FC<BasicButtonProps> = ({label, onClick, color="gray"}) => {
  return (
    <button
      className={`${styles.MenuBotton} ${styles[color]}`}
      onClick={onClick}
    >
      {label}
    </button>
  )
}

const CountryButton: React.FC<CountryButtonProps> = ({label, onClick, buttonType = "LangBotton", country="KR"}) => {
    return (
        <button
            className={`${styles[buttonType]}`}
            onClick={onClick}
        >
            <Flag code={country} style={{ width: 20, height: 10 }} />
            {label}
        </button>
    );
};

export { IconButton, ButtonIcon, BasicButton, CountryButton };

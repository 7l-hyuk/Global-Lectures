// @ts-ignore
import Flag from 'react-world-flags'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ButtonProps, BasicButtonProps, CountryButtonProps } from "../types/components";
import styles from "../styles/Button.module.css";


const IconButton: React.FC<ButtonProps> = ({icon, label, onClick, color = "red", buttonType = "Button"}) => {
    return (
        <button
            className={`${styles[buttonType]} ${styles[color]}`}
            onClick={onClick}
        >
            <FontAwesomeIcon icon={icon} />
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
      className={`${styles.BasicBotton} ${styles[color]}`}
      onClick={onClick}
    >
      {label}
    </button>
  )
}


const CountryButton: React.FC<CountryButtonProps> = ({label, onClick, buttonType = "LangBotton", country="ko"}) => {
    const countryFilter = {
        ko: "KR",
        en: "US",
        ja: "JP",
        zh: "CN"
    };

    return (
        <button
            className={`${styles[buttonType]}`}
            onClick={onClick}
        >
            <Flag code={countryFilter[country]} style={{ width: 20, height: 10 }} />
            {label}
        </button>
    );
};


export { IconButton, ButtonIcon, BasicButton, CountryButton };

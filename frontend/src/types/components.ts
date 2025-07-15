import { IconDefinition } from "@fortawesome/free-solid-svg-icons";


export interface NavbarProps {
  toggleSidebar: () => void;
}


export interface SigninFormGroupProps {
  icon: IconDefinition;
  label: string;
  value: string;
  type: string;
  setValue: (e: string) => void;
}


export interface ButtonProps {
  icon: IconDefinition;
  label: string;
  color?: 'red' | 'green';
  onClick: () => Promise<void> | void;
}
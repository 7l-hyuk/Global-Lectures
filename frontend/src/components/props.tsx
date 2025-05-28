import { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import { User } from "../context/types";


export interface SidebarProps {
    isOpen: boolean;
    user: User | null;
    toggleSidebar: () => void;
}


export interface NavbarProps {
  toggleSidebar: () => void;
}


export interface ButtonProps {
  label: string;
  icon: IconDefinition;
  onClick: () => Promise<void> | void;
  buttonStyle: string;
  disabled: boolean;
}


export interface Styles {
    readonly [key: string]: string;
}

export interface InputProps {
  label: string;
  description: string;
  value: string;
  type: string;
  onChange: (e: string) => void;
  styles: Styles;
}

export interface LoginInputProps {
  label: string;
  value: string;
  type: string;
  onChange: (e: string) => void;
  styles: Styles;
  icon: IconDefinition;
}



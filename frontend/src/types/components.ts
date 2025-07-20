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


export interface SignupFormGroupProps {
  label: string;
  description: string;
  value: string;
  type: string;
  setValue: (e: string) => void;
}


export interface ButtonProps {
  icon: IconDefinition;
  label: string;
  buttonType?: string;
  color?: 'red' | 'green' | 'gray' | 'transparent';
  width?: 'wide' | 'common';
  onClick: () => Promise<void> | void;
}


export interface CountryButtonProps {
  country: 'KR' | 'US' | "JP" | "CN";
  label: string;
  buttonType?: 'Button' | 'UserButton' | 'IndexPageBotton' | 'MenuBotton' | 'LangBotton' | 'ActivatedLangBotton'
  color?: 'red' | 'green' | 'gray' | 'transparent';
  width?: 'wide' | 'common';
  onClick: () => Promise<void> | void;
}


export interface BasicButtonProps {
  label: string;
  color?: 'gray' | 'red';
  onClick: () => Promise<void> | void;
}


export interface VideoProps {
  videoPath: string;
  audioPath: string;
  scriptPath: string;
}


export interface ServiceIntroProps {
  icon: IconDefinition;
  iconColor: string;
  title: string;
  description: string;
}


export interface SubtitleEntry {
  start: number;
  end: number;
  text: string;
}


export interface ScriptContentRowProps {
  script: SubtitleEntry;
}


export interface ControlButtonProps {
  onClick: () => void;
  icon: IconDefinition;
  style: string;
}

export type NavLink = {
    name: string;
    href: string;
};

export interface NavBarProps {
  links: NavLink[];
}
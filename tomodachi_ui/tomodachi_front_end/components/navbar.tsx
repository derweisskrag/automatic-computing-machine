"use client";

import { NavBarProps } from "@/common_types/navProps";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function NavBar({ links }: NavBarProps){
  const currentPath = usePathname();

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="flex justify-between items-center">
        <ul className="flex space-x-4">
          {links.map((link) => (
            <li key={link.name}>
              <Link
                href={link.href}
                className={`px-3 py-2 rounded ${
                  currentPath === link.href
                    ? "bg-blue-600 font-semibold"
                    : "hover:bg-gray-700"
                }`}
              >
                {link.name}
              </Link>
            </li>
          ))}
        </ul>

        {/* TODO: Think of an algorithm what do I want here*/}

        {/* <ul>
          <li>
            <Link
              href={aboutLink.href}
              className={`px-3 py-2 rounded ${
                currentPath === aboutLink.href
                  ? "bg-blue-600 font-semibold"
                  : "hover:bg-gray-700"
              }`}
            >
              {aboutLink.name}
            </Link>
          </li>
        </ul> */}
      </div>
    </nav>
  );
}
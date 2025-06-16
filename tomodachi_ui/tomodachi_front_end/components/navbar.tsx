"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function NavBar() {
  const currentPath = usePathname();

  const links = [
    { name: "Home", href: "/" },
    { name: "Docs", href: "/docs" },
    { name: "Dashboard", href: "/dashboard" },
  ];

  const aboutLink = { name: "About Us", href: "/about" };

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
        <ul>
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
        </ul>
      </div>
    </nav>
  );
}
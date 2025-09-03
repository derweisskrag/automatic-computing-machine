"use client"; 

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LogOut() {
  const router = useRouter();

  useEffect(() => {
    // Simulate clearing cookies/session
    setTimeout(() => {
      router.push("/");
    }, 1500);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-black text-white">
      <svg
        className="animate-spin h-10 w-10 text-blue-500 mb-4"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
        ></path>
      </svg>
      <p className="text-lg">Logging you out...</p>
    </div>
  );
}

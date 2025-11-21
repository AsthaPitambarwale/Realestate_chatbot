import React from "react";
import { Home, Upload, MessageCircle, Moon, Sun } from "lucide-react";

export default function Sidebar({ dark, toggleDark }) {
  return (
    <div className="hidden md:flex flex-col w-64 bg-white dark:bg-gray-800 shadow-lg h-screen fixed left-0 top-0 p-6 space-y-6">
      
      <h1 className="text-2xl font-bold text-gray-800 dark:text-gray-100">
        Real Estate AI
      </h1>

      <nav className="flex flex-col space-y-3 text-gray-700 dark:text-gray-300">
        <div className="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-default">
          <Home size={18} /> Dashboard
        </div>

        <div className="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-default">
          <Upload size={18} /> Upload Dataset
        </div>

        <div className="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-default">
          <MessageCircle size={18} /> Chat & Analysis
        </div>
      </nav>

      <button
        onClick={toggleDark}
        className="flex items-center gap-3 mt-auto p-2 bg-gray-200 dark:bg-gray-700 
        text-gray-800 dark:text-gray-200 rounded-lg hover:opacity-80"
      >
        {dark ? <Sun size={18} /> : <Moon size={18} />}
        {dark ? "Light Mode" : "Dark Mode"}
      </button>
    </div>
  );
}

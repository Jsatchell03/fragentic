// components/Header.jsx
import React from "react";

export default function Header() {
  return (
    <header className="bg-footer text-white py-2">
      <div className="w-full px-8 flex items-center justify-between">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl pr-5">Fragentic</h1>
          <p>AI powered fragrance search</p>
        </div>
        <div>
          <a
            href="#contact" // link to contact section or page
            className="hidden sm:block bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-colors"
          >
            Contact Us
          </a>
        </div>
      </div>
    </header>
  );
}

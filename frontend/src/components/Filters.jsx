import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";

export default function Filters() {
  const API_URL = import.meta.env.VITE_BACKEND_URL;
  useEffect(() => {
    let notes = [];
    let accords = [];
    fetch(`${API_URL}/notes`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        notes = data;
      });
    fetch(`${API_URL}/accords`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        accords = data;
      });
  }, []);
  return (
    <aside
      className="
        w-64
        bg-white
        rounded-xl
        shadow-md
        p-4
        space-y-6
      "
    >
      <h2 className="text-lg font-semibold text-gray-800">Filters</h2>
      <FilterSearch title={"Exclude Notes"} options={[]} />

      <button
        className="
          w-full
          bg-purple-600
          hover:bg-purple-700
          text-white
          font-medium
          py-2
          rounded-lg
          shadow-sm
          focus:outline-none
        "
      >
        Apply Filters
      </button>
    </aside>
  );
}

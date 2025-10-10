import React from "react";
import FilterSearch from "./FilterSearch";

export default function Filters() {
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
      <FilterSearch
        title={"Exclude Notes"}
        options={["Vanilla", "Rose", "Amber"]}
      />

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

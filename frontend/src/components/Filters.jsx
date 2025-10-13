import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";

export default function Filters({
  descriptors,
  notes,
  accords,
  countries,
  brands,
}) {
  const [currFilters, setCurrFilters] = useState({
    "Exclude Descriptors": [],
    "Country of Origin": [],
    Brand: [],
  });

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
        title={"Exclude Descriptors"}
        options={descriptors}
        placeholder={"Search for a descriptor"}
        currFilters={currFilters}
        setCurrFilters={setCurrFilters}
      />
      <FilterSearch
        title={"Country of Origin"}
        options={countries}
        placeholder={"Search for a country"}
        currFilters={currFilters}
        setCurrFilters={setCurrFilters}
      />
      <FilterSearch
        title={"Brand"}
        options={brands}
        placeholder={"Search for a brand"}
        currFilters={currFilters}
        setCurrFilters={setCurrFilters}
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

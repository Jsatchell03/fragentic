import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";
import FilterSelect from "./FilterSelect";
import FilterRating from "./FilterRating";
export default function Filters({
  descriptors,
  notes,
  accords,
  countries,
  brands,
  currQuery,
  setQuery,
}) {
  const [currFilters, setCurrFilters] = useState(currQuery["filters"]);
  function capitalizeBrand(name) {
    return name
      .split("-") // split into words
      .map((word) => word[0].toUpperCase() + word.slice(1)) // capitalize first letter
      .join(" ");
  }
  return (
    <aside
      className="
        w-64
        bg-white
        rounded-xl
        shadow-md
        px-4 py-4
        mx-4
        space-y-6
        mb-16
      "
    >
      <h2 className="text-lg font-semibold text-gray-800">Filters</h2>
      <FilterSelect
        title={"Gender"}
        options={["For Men", "For Women", "Unisex"]}
        currFilters={currFilters}
        setCurrFilters={setCurrFilters}
      />
      <FilterSearch
        title={"Brand"}
        options={brands}
        placeholder={"Search for a brand"}
        currFilters={currFilters}
        setCurrFilters={setCurrFilters}
        optionCleaner={capitalizeBrand}
      />
      <FilterRating
        title={"Rating"}
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
        title={"Exclude Notes/Accords"}
        options={descriptors}
        placeholder={"Search for a note/accord"}
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
        onClick={() => {
          if (
            JSON.stringify(currFilters) != JSON.stringify(currQuery.filters)
          ) {
            setQuery({ ...currQuery, filters: currFilters });
          } else {
            console.log("Filters unchanged — no query update needed");
          }
        }}
      >
        Apply Filters
      </button>
    </aside>
  );
}

import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";
import FilterSelect from "./FilterSelect";
import FilterRating from "./FilterRating";
import FilterRange from "./FilterRange";
export default function Filters({
  descriptors,
  notes,
  accords,
  countries,
  brands,
  currQuery,
  selectedFilters,
  setSelectedFilters,
  updateQuery,
}) {
  const currFilters = selectedFilters || {
    "Exclude Notes/Accords": [],
    "Country of Origin": [],
    Brand: [],
    Gender: [],
    Popularity: [],
    PopularityRange: [],
    Rating: 1,
  };
  function capitalizeBrand(name) {
    return name
      .split("-") // split into words
      .map((word) => word[0].toUpperCase() + word.slice(1)) // capitalize first letter
      .join(" ");
  }

  function cleanCountryName(name) {
    return name.toUpperCase();
  }

  return (
    <>
      <div
        className="
        w-64
        bg-white
        rounded-xl
        shadow-md
        px-4 py-4
        mx-4
        space-y-6
      "
      >
        <h2 className="text-lg font-semibold text-gray-800">Filters</h2>
        <FilterSelect
          title={"Gender"}
          options={["For Men", "For Women", "Unisex"]}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
        />
        <FilterSearch
          title={"Brand"}
          options={brands}
          placeholder={"Search for a brand"}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
          optionCleaner={capitalizeBrand}
        />
        <FilterRating
          title={"Rating"}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
        />
        <FilterSearch
          title={"Country of Origin"}
          options={countries}
          placeholder={"Search for a country"}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
          optionCleaner={cleanCountryName}
        />
        <FilterRange
          title={"Popularity"}
          options={["Obscure", "Uncommon", "Moderate", "Well-Known", "Common"]}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
        />
        <FilterSearch
          title={"Exclude Notes/Accords"}
          options={descriptors}
          placeholder={"Search for a note/accord"}
          currFilters={currFilters}
          setCurrFilters={setSelectedFilters}
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
            updateQuery({ ...currQuery, filters: currFilters });
          }}
        >
          Apply Filters
        </button>
      </div>
    </>
  );
}

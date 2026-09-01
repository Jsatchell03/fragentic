import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";
import FilterSelect from "./FilterSelect";
import FilterRating from "./FilterRating";
import FilterRange from "./FilterRange";
import { DESCRIPTORS, COUNTRIES, BRANDS } from "../constants.js";

export default function Filters({ queryFilters, updateQuery }) {
  const currFilters = selectedFilters || {
    "Exclude Notes/Accords": [],
    "Country of Origin": [],
    Brand: [],
    Gender: [],
    Popularity: [],
    PopularityRange: [],
    Rating: 1,
  };

  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedGender, setSelectedGender] = useState([]);
  const [minRating, setMinRating] = useState(0);
  const [selectedCountries, setSelectedCountries] = useState([]);
  const [excludedDescriptors, setExcludedDescriptors] = useState([]);
  const [popularityRange, setPopularityRange] = useState([]);

  function capitalizeBrand(name) {
    return name
      .split("-")
      .map((word) => word[0].toUpperCase() + word.slice(1))
      .join(" ");
  }

  function cleanCountryName(name) {
    if (name === "usa" || name === "uk" || name === "uae") {
      return name.toUpperCase();
    } else {
      let arr = name.split(" ");
      arr = arr.map((x) => {
        let newStr = "";
        newStr += x[0].toUpperCase();
        newStr += x.slice(1);
        return newStr;
      });
      return arr.join(" ");
    }
  }

  return (
    <div className="w-full bg-white rounded-xl shadow-md px-4 py-4 space-y-6">
      <h2 className="text-lg font-semibold text-gray-800">Filters</h2>

      <FilterSelect
        title={"Gender"}
        options={["For Men", "For Women", "Unisex"]}
        currFilters={currFilters}
        setCurrFilters={setSelectedFilters}
      />

      <FilterSearch
        title={"Brand"}
        options={BRANDS}
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
        options={COUNTRIES}
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
        options={DESCRIPTORS}
        placeholder={"Search for a note/accord"}
        currFilters={currFilters}
        setCurrFilters={setSelectedFilters}
      />

      <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 rounded-lg shadow-sm focus:outline-none transition-colors">
        Apply Filters
      </button>
    </div>
  );
}

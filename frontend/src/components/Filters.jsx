import React, { useState, useEffect } from "react";
import FilterSearch from "./FilterSearch";
import FilterSelect from "./FilterSelect";
import FilterRating from "./FilterRating";
import FilterRange from "./FilterRange";
import { DESCRIPTORS, COUNTRIES, BRANDS } from "../constants.js";

export default function Filters({ queryFilters, updateQuery }) {
  const [selectedBrands, setSelectedBrands] = useState(queryFilters.brands);
  const [selectedGenders, setSelectedGenders] = useState(queryFilters.genders);
  const [minRating, setMinRating] = useState(queryFilters.rating);
  const [selectedCountries, setSelectedCountries] = useState(
    queryFilters.countries,
  );
  const [excludedDescriptors, setExcludedDescriptors] = useState(
    queryFilters.excludedDescriptors,
  );
  const [popularityRange, setPopularityRange] = useState(
    queryFilters.popularity,
  );

  const arraysAreDiff = (arr1, arr2) => {
    if (arr1.length !== arr2.length) return true;
    const sorted1 = [...arr1].sort();
    const sorted2 = [...arr2].sort();
    return sorted1.some((val, idx) => val !== sorted2[idx]);
  };

  const buttonActive =
    arraysAreDiff(selectedBrands, queryFilters.brands) ||
    arraysAreDiff(selectedGenders, queryFilters.genders) ||
    arraysAreDiff(selectedCountries, queryFilters.countries) ||
    arraysAreDiff(excludedDescriptors, queryFilters.excludedDescriptors) ||
    arraysAreDiff(popularityRange, queryFilters.popularity) ||
    minRating !== queryFilters.rating;

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
        currValue={selectedGenders}
        setCurrValue={setSelectedGenders}
      />

      <FilterSearch
        title={"Brand"}
        options={BRANDS}
        placeholder={"Search for a brand"}
        currValue={selectedBrands}
        setCurrValue={setSelectedBrands}
        optionCleaner={capitalizeBrand}
      />

      <FilterRating
        title={"Rating"}
        currValue={minRating}
        setCurrValue={setMinRating}
      />

      <FilterSearch
        title={"Country of Origin"}
        options={COUNTRIES}
        placeholder={"Search for a country"}
        currValue={selectedCountries}
        setCurrValue={setSelectedCountries}
        optionCleaner={cleanCountryName}
      />

      {/* <FilterRange
        title={"Popularity"}
        options={["Obscure", "Uncommon", "Moderate", "Well-Known", "Common"]}
        currValue={popularityRange}
        setCurrFilters={setPopularityRange}
      /> */}

      <FilterSearch
        title={"Exclude Notes/Accords"}
        options={DESCRIPTORS}
        placeholder={"Search for a note/accord"}
        currValue={excludedDescriptors}
        setCurrValue={setExcludedDescriptors}
      />

      <button
        className={`w-full ${buttonActive ? "bg-purple-600 hover:bg-purple-700 cursor-pointer" : "bg-gray-300"} text-white font-medium py-2 rounded-lg shadow-sm focus:outline-none transition-colors`}
        onClick={() => {
          if (buttonActive) {
            updateQuery({
              brands: selectedBrands,
              countries: selectedCountries,
              genders: selectedGenders,
              excludedDescriptors: excludedDescriptors,
              rating: minRating,
              popularity: popularityRange,
            });
          }
        }}
      >
        Apply Filters
      </button>
    </div>
  );
}

import React, { useState } from "react";
import FilterSearch from "./FilterSearch";
import FilterSelect from "./FilterSelect";
import FilterRating from "./FilterRating";
import FilterRange from "./FilterRange";
import { DESCRIPTORS, COUNTRIES, BRANDS } from "../constants.js";

export default function Filters({
  initialFilters,
  filtersActive,
  updateCurrQuery,
  executeFilters,
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedBrands, setSelectedBrands] = useState(initialFilters.brands);
  const [selectedGenders, setSelectedGenders] = useState(
    initialFilters.genders,
  );
  const [minRating, setMinRating] = useState(initialFilters.rating);
  const [selectedCountries, setSelectedCountries] = useState(
    initialFilters.countries,
  );
  const [excludedDescriptors, setExcludedDescriptors] = useState(
    initialFilters.excludedDescriptors,
  );
  const [popularityRange, setPopularityRange] = useState(
    initialFilters.popularity,
  );

  const handleBrandsChange = (v) => {
    setSelectedBrands(v);
    updateCurrQuery({ brands: v });
  };

  const handleGendersChange = (v) => {
    setSelectedGenders(v);
    updateCurrQuery({ genders: v });
  };

  const handleRatingChange = (v) => {
    setMinRating(v);
    updateCurrQuery({ rating: v });
  };

  const handleCountriesChange = (v) => {
    setSelectedCountries(v);
    updateCurrQuery({ countries: v });
  };

  const handlePopularityChange = (v) => {
    setPopularityRange(v);
    updateCurrQuery({ popularity: v });
  };

  const handleExcludedDescriptorsChange = (v) => {
    setExcludedDescriptors(v);
    updateCurrQuery({ excludedDescriptors: v });
  };

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
    <div className="w-full bg-white rounded-xl shadow-md px-4 py-4">
      <button
        className="md:hidden w-full flex justify-between items-center text-lg font-semibold text-gray-800 mb-0"
        onClick={() => setIsOpen((o) => !o)}
      >
        <span>Filters</span>
        <span className="text-gray-500 text-base">{isOpen ? "▴" : "▾"}</span>
      </button>
      <h2 className="hidden md:block text-lg font-semibold text-gray-800 mb-6">Filters</h2>

      <div className={`${isOpen ? "block" : "hidden"} md:block space-y-6 mt-4 md:mt-0`}>

      <FilterSelect
        title={"Gender"}
        options={["For Men", "For Women", "Unisex"]}
        currValue={selectedGenders}
        setCurrValue={handleGendersChange}
      />

      <FilterSearch
        title={"Brand"}
        options={BRANDS}
        placeholder={"Search for a brand"}
        currValue={selectedBrands}
        setCurrValue={handleBrandsChange}
        optionCleaner={capitalizeBrand}
      />

      <FilterRating
        title={"Rating"}
        currValue={minRating}
        setCurrValue={handleRatingChange}
      />

      <FilterSearch
        title={"Country of Origin"}
        options={COUNTRIES}
        placeholder={"Search for a country"}
        currValue={selectedCountries}
        setCurrValue={handleCountriesChange}
        optionCleaner={cleanCountryName}
      />

      <FilterRange
        title={"Popularity"}
        options={["Obscure", "Uncommon", "Moderate", "Well-Known", "Common"]}
        currValue={popularityRange}
        setCurrValue={handlePopularityChange}
      />

      <FilterSearch
        title={"Exclude Notes/Accords"}
        options={DESCRIPTORS}
        placeholder={"Search for a note/accord"}
        currValue={excludedDescriptors}
        setCurrValue={handleExcludedDescriptorsChange}
      />

      <button
        className={`w-full ${filtersActive ? "bg-purple-600 hover:bg-purple-700 cursor-pointer" : "bg-gray-300"} text-white font-medium py-2 rounded-lg shadow-sm focus:outline-none transition-colors`}
        onClick={() => {
          if (filtersActive) {
            executeFilters();
          }
        }}
      >
        Apply Filters
      </button>
      </div>
    </div>
  );
}

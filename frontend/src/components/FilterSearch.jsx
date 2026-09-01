import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Tag from "./Tag";

export default function FilterSearch({
  title,
  options,
  placeholder,
  currValue,
  setCurrValue,
  optionCleaner,
}) {
  const updateFilters = (option) => {
    setCurrValue([...currValue, option]);
  };

  const toggleOption = (option) => {
    setCurrValue(currValue.filter((o) => o !== option));
  };

  return (
    <div className="mb-5">
      <p className="mb-2">{title}</p>
      {currValue.length > 0 &&
        currValue.map((option) => (
          <Tag
            name={option}
            key={option}
            removeTag={() => toggleOption(option)}
            optionCleaner={optionCleaner}
          />
        ))}
      <SearchBar
        selectedOptions={currValue}
        updateSelectedOptions={updateFilters}
        options={options}
        optionCleaner={optionCleaner}
        placeholder={placeholder}
      />
    </div>
  );
}

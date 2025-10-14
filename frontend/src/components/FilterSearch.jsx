import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Tag from "./Tag";

export default function FilterSearch({
  title,
  options,
  placeholder,
  currFilters,
  setCurrFilters,
  optionCleaner,
}) {
  const [selectedOptions, setSelectedOptions] = useState(currFilters[title]);

  const updateFilters = (option) => {
    const newSelectedOptions = [...selectedOptions, option];
    setSelectedOptions(newSelectedOptions);

    const newFilters = { ...currFilters, [title]: newSelectedOptions };
    setCurrFilters(newFilters);
  };

  const toggleOption = (option) => {
    const newSelected = selectedOptions.filter((o) => o !== option);
    setSelectedOptions(newSelected);
    const newFilters = { ...currFilters, [title]: newSelected };
    setCurrFilters(newFilters);
  };

  return (
    <div className="mb-5">
      <p className="mb-2">{title}</p>
      {selectedOptions.length > 0 &&
        selectedOptions.map((option) => (
          <Tag
            name={option}
            key={option}
            removeTag={() => toggleOption(option)}
            optionCleaner={optionCleaner}
          />
        ))}
      <SearchBar
        selectedOptions={selectedOptions}
        updateSelectedOptions={updateFilters}
        options={options}
        optionCleaner={optionCleaner}
        placeholder={placeholder}
      />
    </div>
  );
}

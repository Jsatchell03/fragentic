import React, { useState } from "react";

export default function FilterSelect({
  title,
  options,
  currFilters,
  setCurrFilters,
}) {
  const selected = currFilters[title] || [];

  const toggleOption = (option) => {
    const newSelected = selected.includes(option)
      ? selected.filter((x) => x !== option)
      : [...selected, option];

    setCurrFilters({ ...currFilters, [title]: newSelected });
  };

  return (
    <div>
      <p className="mb-2">{title}</p>
      <div className="px-2">
        <ul>
          {options.map((option) => (
            <li
              className="flex items-center space-x-2"
              key={option}
              onClick={() => toggleOption(option)}
            >
              <input
                className=" w-5 h-5 accent-purple-600 rounded cursor-pointer border-10 hover:border-purple-700"
                type="checkbox"
                checked={selected.includes(option)}
                readOnly={true}
              ></input>
              <label>{option}</label>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

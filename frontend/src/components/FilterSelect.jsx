import React, { useState } from "react";

export default function FilterSelect({
  title,
  options,
  currValue,
  setCurrValue,
}) {
  const toggleOption = (option) => {
    setCurrValue(
      currValue.includes(option)
        ? currValue.filter((x) => x !== option)
        : [...currValue, option],
    );
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
                checked={currValue.includes(option)}
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

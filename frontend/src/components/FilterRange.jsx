import React from "react";
import Tag from "./Tag";

export default function FilterRange({ title, options, currValue, setCurrValue }) {
  const optionMaping = {};
  options.forEach((option, indx) => {
    optionMaping[option] = indx + 1;
  });

  const selected = currValue || [];

  const getFilterRange = (selected) => {
    if (selected.length === 0) return [];
    let newFilterRange = [[selected[0], selected[0]]];
    for (let i = 1; i < selected.length; i++) {
      let match = false;
      for (let j = 0; j < newFilterRange.length; j++) {
        if (newFilterRange[j][1] === selected[i] - 1) {
          newFilterRange[j][1] = selected[i];
          match = true;
          break;
        }
      }
      if (!match) {
        newFilterRange.push([selected[i], selected[i]]);
      }
    }
    return newFilterRange;
  };

  const filterRange = getFilterRange(selected);

  const toggleOption = (option) => {
    const newSelected = selected.includes(optionMaping[option])
      ? selected.filter((x) => x !== optionMaping[option]).sort((a, b) => a - b)
      : [...selected, optionMaping[option]].sort((a, b) => a - b);
    setCurrValue(newSelected);
  };

  return (
    <div>
      <p className="mb-2">{title}</p>
      <div className="flex flex-wrap">
        {filterRange.map((range, index) => (
          <Tag
            key={index}
            removeTag={(r) => {
              const newSelected = selected.filter((s) => s < r[0] || s > r[1]);
              setCurrValue(newSelected);
            }}
            optionCleaner={(r) =>
              r[0] === r[1]
                ? options[r[0] - 1]
                : options[r[0] - 1] + " to " + options[r[1] - 1]
            }
            name={range}
          />
        ))}
      </div>
      <div className="px-2 mt-2">
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
                checked={selected.includes(optionMaping[option])}
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

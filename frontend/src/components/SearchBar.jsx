import React, { useState, useEffect, useRef } from "react";

export default function SearchBar({
  selectedOptions,
  updateSelectedOptions,
  triggerSearch = null,
  optionCleaner = null,
  options,
  placeholder,
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredOptions, setFilteredOptions] = useState(
    options.filter((option) => !selectedOptions.includes(option.toLowerCase()))
  );
  const [isOpen, setIsOpen] = useState(false);
  const wrapperRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm("");
      }
    };

    const handleEscape = (event) => {
      if (event.key === "Escape") {
        setIsOpen(false);
        setSearchTerm("");
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, []);

  const handleChange = (e) => {
    const val = e.target.value;
    setSearchTerm(val);
    if (val.length > 0) {
      const newFilteredOptions = options.filter(
        (option) =>
          option.toLowerCase().includes(val.toLowerCase()) &&
          !selectedOptions.includes(option.toLowerCase())
      );
      setFilteredOptions(newFilteredOptions.slice(0, 5));
    } else {
      setFilteredOptions(
        options
          .filter((option) => !selectedOptions.includes(option.toLowerCase()))
          .slice(0, 5)
      );
    }
    setIsOpen(true);
  };

  const handleSelect = (val) => {
    updateSelectedOptions(val);
    setSearchTerm("");
    setIsOpen(false);
  };

  return (
    <div ref={wrapperRef} className="relative w-full flex">
      <div
        className="
          relative w-full
          rounded-xl 
          border border-gray-300 
          shadow-sm
          focus-within:border-purple-600 
          transition
        "
      >
        <input
          type="text"
          onChange={handleChange}
          value={searchTerm}
          placeholder={placeholder}
          className={`
            w-full
            rounded-xl
            px-4 py-3 ${triggerSearch && "pr-24"}
            text-gray-700 
            placeholder-gray-400 
            focus:outline-none
          `}
        />
        {triggerSearch && (
          <button
            onClick={triggerSearch}
            className="
            absolute top-1/2 right-2 -translate-y-1/2
            bg-purple-600 
            hover:bg-purple-700 
            text-white 
            font-medium 
            px-4 py-2 
            rounded-xl 
            shadow-sm
          "
          >
            Search
          </button>
        )}
      </div>

      {isOpen && filteredOptions.length > 0 && searchTerm.length > 0 && (
        <ul
          className="
            absolute top-full left-0 mt-2 w-full 
            bg-white 
            border border-gray-200 
            rounded-xl 
            shadow-lg 
            z-10
            max-h-60 overflow-y-auto
          "
        >
          {filteredOptions.map((option, index) => (
            <li
              key={index}
              onClick={() => handleSelect(option)}
              className="
                px-4 py-2 
                text-gray-700 
                hover:bg-purple-50 hover:text-purple-700 
                cursor-pointer
              "
            >
              {optionCleaner ? optionCleaner(option) : option}
            </li>
          ))}
        </ul>
      )}

      {isOpen && filteredOptions.length === 0 && searchTerm.length > 0 && (
        <div
          className="
            absolute top-full left-0 mt-2 w-full 
            bg-white 
            border border-gray-200 
            rounded-xl 
            shadow-lg 
            px-4 py-2 z-10
            text-gray-500
          "
        >
          No matching options found.
        </div>
      )}
    </div>
  );
}

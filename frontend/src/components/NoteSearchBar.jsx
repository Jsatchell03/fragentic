import React, { useState, useEffect } from "react";

export default function NoteSearchBar(props) {
  const selectedNotes = props.selectedNotes;
  const setSelectedNotes = props.setSelectedNotes;
  const [searchTerm, setSearchTerm] = useState("");
  const API_URL = import.meta.env.REACT_APP_BACKEND_URL;
  useEffect(() => {
    let notes = [];
    let accords = [];
    fetch(`${API_URL}/notes`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        notes = data;
      });
    fetch(`${API_URL}/accords`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        accords = data;
      });
  }, []);
  const [filteredOptions, setFilteredOptions] = useState(
    options.filter((option) => !selectedNotes.includes(option.toLowerCase()))
  );
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (e) => {
    const val = e.target.value;
    setSearchTerm(val);
    if (val.length > 0) {
      const newFilteredOptions = options.filter(
        (option) =>
          option.toLowerCase().includes(val.toLowerCase()) &&
          !selectedNotes.includes(option.toLowerCase())
      );
      setFilteredOptions(newFilteredOptions.slice(0, 5));
    } else {
      setFilteredOptions(
        options
          .filter((option) => !selectedNotes.includes(option.toLowerCase()))
          .slice(0, 5)
      );
    }
    setIsOpen(true);
  };

  const handleSelect = (val) => {
    setSelectedNotes([...selectedNotes, val]);
    setSearchTerm("");
    setIsOpen(false);
  };

  return (
    <div className="relative w-full flex">
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
          placeholder="Type a fragrance note (e.g., vanilla, rose, sandalwood)..."
          className="
            w-full
            rounded-xl
            px-4 py-3 pr-24
            text-gray-700 
            placeholder-gray-400 
            focus:outline-none
          "
        />
        <button
          onClick={props.triggerSearch}
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
      </div>

      {isOpen && filteredOptions.length > 0 && (
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
              {option}
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
            px-4 py-2 
            text-gray-500
          "
        >
          No matching notes found.
        </div>
      )}
    </div>
  );
}

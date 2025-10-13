import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Tag from "./Tag";

export default function NoteSearch({ descriptors }) {
  const [selectedNotes, setSelectedNotes] = useState([]);

  const removeNote = (note) => {
    setSelectedNotes(selectedNotes.filter((n) => n !== note));
  };

  const updateSelectedNotes = (note) => {
    let newSelectedNotes = [...selectedNotes, note];
    setSelectedNotes(newSelectedNotes);
  };

  const search = () => {
    console.log(selectedNotes);
  };

  return (
    <div
      className="
        bg-white
        rounded-xl
        shadow-md
        mx-5
        my-5 p-4
      "
    >
      <h2 className="text-lg font-semibold text-gray-800 pb-6">
        Find your fragrance
      </h2>

      <p>
        Descibe the notes and accords of your fragrance and Fragentic will find
        the top matches
      </p>
      {selectedNotes.length > 0 &&
        selectedNotes.map((note, index) => (
          <Tag name={note} key={index} removeTag={removeNote} />
        ))}
      <SearchBar
        selectedOptions={selectedNotes}
        updateSelectedOptions={updateSelectedNotes}
        triggerSearch={search}
        options={descriptors}
      />
    </div>
  );
}

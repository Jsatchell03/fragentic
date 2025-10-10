import React, { useState } from "react";
import NoteSearchBar from "./NoteSearchBar";
import NoteTag from "./NoteTag";

export default function NoteSearch() {
  const [selectedNotes, setSelectedNotes] = useState([]);

  const removeNote = (note) => {
    setSelectedNotes(selectedNotes.filter((n) => n !== note));
  };

  const search = () => {
    console.log(selectedNotes);
  };

  return (
    <div>
      <h1>Find your fragrance</h1>
      <p>
        Descibe the notes of your fragrance and Fragentic will find the top
        matches
      </p>
      {selectedNotes.length > 0 &&
        selectedNotes.map((note, index) => (
          <NoteTag note={note} key={index} removeNote={removeNote} />
        ))}
      <NoteSearchBar
        selectedNotes={selectedNotes}
        setSelectedNotes={setSelectedNotes}
        triggerSearch={search}
      />
    </div>
  );
}

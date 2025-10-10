import React from "react";

export default function NoteTag({ note, removeNote }) {
  return (
    <span
      className="
        inline-flex
        items-center 
        px-3 py-1 
        text-sm
        font-medium 
        text-purple-700 
        bg-purple-100 
        rounded-full 
        hover:bg-purple-200 
        mr-2 mb-2
      "
    >
      {note}
      <button
        onClick={() => removeNote(note)}
        className="
          ml-2 
          text-purple-500 hover:text-purple-700 
          focus:outline-none
        "
      >
        x
      </button>
    </span>
  );
}

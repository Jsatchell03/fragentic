import React from "react";

export default function ButtonTag({ name, action, optionCleaner = null }) {
  return (
    <span
      onClick={action}
      className="
      inline-flex
      items-center
      px-3 py-1
      text-sm
      font-medium
      text-purple-700
      bg-gray-100
      rounded-full
      hover:bg-purple-200
      mr-2 mt-2
      whitespace-nowrap
      overflow-hidden
      text-ellipsis
      max-w-[200px]
    "
    >
      <span className="truncate">
        {optionCleaner ? optionCleaner(name) : name}
      </span>
    </span>
  );
}

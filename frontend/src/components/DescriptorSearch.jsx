import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Tag from "./Tag";

export default function DescriptorSearch({ descriptors, setQuery, currQuery }) {
  const [selectedDescriptors, setSelectedDescriptors] = useState([]);

  const removeDescriptor = (descriptor) => {
    setSelectedDescriptors(selectedDescriptors.filter((n) => n !== descriptor));
  };

  const updateselectedDescriptors = (descriptor) => {
    let newSelectedDescriptors = [...selectedDescriptors, descriptor];
    setSelectedDescriptors(newSelectedDescriptors);
  };

  const search = () => {
    if (
      JSON.stringify(selectedDescriptors) !=
      JSON.stringify(currQuery.descriptors)
    ) {
      setQuery({ ...currQuery, descriptors: selectedDescriptors });
    } else {
      console.log("Descriptors unchanged — no query update needed");
    }
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
      {selectedDescriptors.length > 0 &&
        selectedDescriptors.map((descriptor, index) => (
          <Tag name={descriptor} key={index} removeTag={removeDescriptor} />
        ))}
      <SearchBar
        selectedOptions={selectedDescriptors}
        updateSelectedOptions={updateselectedDescriptors}
        triggerSearch={search}
        options={descriptors}
      />
    </div>
  );
}

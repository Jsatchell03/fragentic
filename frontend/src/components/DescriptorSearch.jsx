import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Tag from "./Tag";
import ButtonTag from "./ButtonTag";
import { DESCRIPTORS } from "../constants.js";

export default function DescriptorSearch({ queryDescriptors, updateQuery }) {
  const [currDescriptors, setCurrDescriptors] = useState(
    queryDescriptors || [],
  );

  const commonDescriptors = [
    "wood",
    "citrus",
    "powdery",
    "sweet",
    "amber",
    "aromatic",
    "musk",
    "floral",
    "warm spicy",
    "fruity",
    "fresh spicy",
    "vanilla",
    "musky",
    "white floral",
    "bergamot",
    "sandalwood",
    "rose",
    "jasmine",
    "patchouli",
    "fresh",
    "green",
    "cedar",
    "earthy",
    "mandarin orange",
    "vetiver",
    "balsamic",
    "tonka bean",
    "lemon",
    "iris",
    "soft spicy",
    "violet",
    "animalic",
    "leather",
    "lavender",
    "lily of the valley",
    "orange blossom",
    "pink pepper",
    "cardamom",
    "grapefruit",
    "aquatic",
    "ylang-ylang",
    "geranium",
    "oakmoss",
    "peach",
    "herbal",
    "freesia",
    "white musk",
    "yellow floral",
    "benzoin",
    "cinnamon",
  ].filter((n) => !currDescriptors.includes(n));

  const removeDescriptor = (descriptor) => {
    setCurrDescriptors([...currDescriptors].filter((n) => n !== descriptor));
  };

  const addDescriptor = (descriptor) => {
    setCurrDescriptors([...currDescriptors, descriptor]);
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

      <p>Descibe your scent and Fragentic will find the top matches</p>

      {currDescriptors.length > 0 &&
        currDescriptors.map((descriptor, index) => (
          <Tag name={descriptor} key={index} removeTag={removeDescriptor} />
        ))}

      <SearchBar
        selectedOptions={currDescriptors}
        updateSelectedOptions={addDescriptor}
        triggerSearch={() => updateQuery(currDescriptors)}
        options={DESCRIPTORS}
        name={"descriptor-search"}
        active={
          !(
            currDescriptors.length === 0 ||
            (queryDescriptors !== null &&
              currDescriptors.length === queryDescriptors.length &&
              [...currDescriptors]
                .sort()
                .every(
                  (val, index) => val === [...queryDescriptors].sort()[index],
                ))
          )
        }
      />

      <div className="mt-2">
        <p className="mb-2">Most common notes and accords</p>
        {commonDescriptors.slice(0, 10).map((descriptor, index) => {
          return (
            <ButtonTag
              key={index}
              name={descriptor}
              action={() => addDescriptor(descriptor)}
            />
          );
        })}
      </div>
    </div>
  );
}

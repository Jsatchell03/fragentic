import React, { useState } from "react";
const options = [
  "tobacco leaf",
  "datura",
  "lactonic",
  "pelargonium",
  "peony",
  "neroli",
  "styrax",
  "musk",
  "orange peel",
  "cotton candy",
  "bulrush",
  "spices",
  "rose",
  "whipped cream",
  "chamomile",
  "geranium",
  "sugar cane",
  "white woods",
  "vanilla",
  "woodsy notes",
  "turkish rose",
  "paprika",
  "papyrus",
  "green tea",
  "kiwi",
  "tagetes",
  "clover",
  "labdanum",
  "watermelon",
  "cashmere wood",
  "caraway",
  "green leaves",
  "blackberry",
  "water hyacinth",
  "tomato",
  "balsamic",
  "bourbon geranium",
  "amberwood",
  "teak wood",
  "cognac",
  "violet",
  "green grass",
  "green mandarin",
  "water notes",
  "himalayan poppy",
  "saffron",
  "vanilla bean",
  "sichuan pepper",
  "bamboo",
  "chocolate",
  "lemon",
  "yellow floral",
  "citrus",
  "magnolia",
  "fresh",
  "mossy",
  "sour cherry",
  "juniper berries",
  "sea water",
  "mysore sandalwood",
  "rhubarb",
  "carrot seeds",
  "cardamom",
  "mahogany",
  "flint",
  "carnation",
  "cedarwood",
  "osmanthus",
  "elemi",
  "animalic",
  "cupcake",
  "white musk",
  "cassis",
  "gardenia",
  "granny smith apple",
  "lemon tree",
  "green mango",
  "lilac",
  "violet leaf",
  "opoponax",
  "freesia",
  "ambergris",
  "hyacinth",
  "guaiac wood",
  "passion flower",
  "ivy",
  "sea notes",
  "cloves",
  "orange blossom",
  "metallic",
  "celery seeds",
  "parma violet",
  "vetiver",
  "night blooming cereus",
  "nutty",
  "atlas cedar",
  "black vanilla husk",
  "amber",
  "apple",
  "mango",
  "floral",
  "powdery notes",
  "rose de mai",
  "ozonic",
  "hawthorn",
  "sicilian mandarin",
  "cassia",
  "honey",
  "vanilla flower",
  "pear",
  "tuberose",
  "yuzu",
  "petitgrain",
  "apricot blossom",
  "truffle",
  "white rose",
  "italian orange",
  "tarragon",
  "ambroxan",
  "sweet",
  "red litchi",
  "salt",
  "orchid",
  "coffee",
  "blue lotus",
  "anis",
  "musk mallow",
  "melon",
  "mate",
  "licorice",
  "white floral",
  "tea",
  "strawberry",
  "orris",
  "spicy notes",
  "aquatic",
  "mint",
  "carrot",
  "cyclamen",
  "indian patchouli",
  "bellflower",
  "raspberry",
  "champaca",
  "apricot",
  "persimmon",
  "nutmeg",
  "cedar",
  "litchi",
  "jasmine sambac",
  "lily-of-the-valley",
  "sicilian lemon",
  "lime",
  "mandarin orange",
  "lotus",
  "black orchid",
  "peru balsam",
  "herbal",
  "amalfi lemon",
  "heliotrope",
  "virginian cedar",
  "black currant",
  "coriander",
  "leather",
  "grapefruit",
  "french labdanum",
  "fig leaf",
  "warm spicy",
  "smoky",
  "dried fruits",
  "birch",
  "bergamot",
  "citruses",
  "powdery",
  "coumarin",
  "clary sage",
  "orange",
  "calabrian bergamot",
  "apple tree",
  "anise",
  "red currant",
  "benzoin",
  "cherry",
  "citron",
  "sycamore",
  "calone",
  "black violet",
  "silk tree blossom",
  "incense",
  "orris root",
  "aldehydic",
  "jasmine",
  "green",
  "green notes",
  "rosemary",
  "rum",
  "pomegranate",
  "ylang-ylang",
  "hiacynth",
  "vanille",
  "mignonette",
  "cacao",
  "fruity notes",
  "brown sugar",
  "tangerine",
  "narcissus",
  "thanaka wood",
  "cinnamon",
  "black cherry",
  "amaryllis",
  "pepper",
  "plum",
  "black pepper",
  "cashmeran",
  "caramel",
  "bitter almond",
  "vanilla orchid",
  "earthy",
  "peach",
  "papaya",
  "lavender",
  "oakmoss",
  "madagascar vanilla",
  "fresh spicy",
  "tahitian vanilla",
  "cumin",
  "salty",
  "blood mandarin",
  "iso e super",
  "tea rose",
  "white amber",
  "aromatic",
  "cherry liqueur",
  "marine",
  "cypress",
  "ginger",
  "iris",
  "wild berries",
  "lily",
  "australian sandalwood",
  "blood grapefruit",
  "quince",
  "green accord",
  "coconut",
  "may rose",
  "elemi resin",
  "musky",
  "star fruit",
  "tropical",
  "oak",
  "woody",
  "oriental notes",
  "fir resin",
  "green apple",
  "nutmeg flower",
  "brazilian rosewood",
  "juniper",
  "oak moss",
  "artemisia",
  "aldehydes",
  "pineapple",
  "chestnut",
  "java vetiver oil",
  "sandalwood",
  "mandarin leaf",
  "moss",
  "bulgarian rose",
  "water jasmine",
  "ceylon cinnamon",
  "haitian vetiver",
  "tahitian vetiver",
  "cucumber",
  "fruity",
  "fennel",
  "tobacco",
  "civet",
  "patchouli",
  "mexican chocolate",
  "mimosa",
  "ice",
  "white chocolate",
  "pink pepper",
  "tonka bean",
  "almond",
  "thyme",
  "woody notes",
  "african orange flower",
  "white honey",
  "basil",
  "moroccan jasmine",
  "passionfruit",
  "tobacco blossom",
  "star anise",
  "sage",
  "rhuburb",
  "black rose",
  "soft spicy",
  "honeysuckle",
  "ginger flower",
  "praline",
  "lemon verbena",
  "bitter orange",
  "red berries",
  "olibanum",
  "wallflower",
  "virginia cedar",
];

export default function NoteSearchBar(props) {
  const selectedNotes = props.selectedNotes;
  const setSelectedNotes = props.setSelectedNotes;
  const [searchTerm, setSearchTerm] = useState("");
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

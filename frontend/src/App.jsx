import { useState, useEffect } from "react";
import NoteSearch from "./components/NoteSearch";
import Filters from "./components/Filters";

function App() {
  const API_URL = import.meta.env.VITE_BACKEND_URL;
  const [allNotes, setAllNotes] = useState([
    "vanilla",
    "apple",
    "citrus",
    "lavender",
    "cedar wood",
  ]);
  const [allAccords, setAllAccords] = useState([
    "woody",
    "sweet",
    "spicy",
    "musky",
    "fresh",
  ]);
  const [allCountries, setAllCountries] = useState([
    "us",
    "uae",
    "france",
    "italy",
    "uk",
  ]);
  const [allBrands, setAllBrands] = useState([
    "Dior",
    "Valentino",
    "Gucci",
    "Nautica",
    "Versace",
  ]);
  const [descriptors, setDescriptors] = useState(allAccords.concat(allNotes));
  const [advancedSearch, setAdvancedSearch] = useState(false);

  // useEffect(() => {
  //   fetch(`${API_URL}/filters`)
  //     .then((res) => res.json())
  //     .then((data) => {
  //       console.log(data);
  //       setAllNotes(data["notes"]);
  //       setAllAccords(data["accords"]);
  //       setAllCountries(data["countries"]);
  //       setAllBrands(data["brands"]);
  //       setDescriptors(data["descriptors"]);
  //     });
  // }, []);

  return (
    <>
      <NoteSearch descriptors={descriptors} />
      <Filters
        descriptors={descriptors}
        accords={allAccords}
        notes={allNotes}
        brands={allBrands}
        countries={allCountries}
      />
    </>
  );
}

export default App;

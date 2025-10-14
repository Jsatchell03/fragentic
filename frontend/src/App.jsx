import { useState, useEffect, useRef } from "react";
import DescriptorSearch from "./components/DescriptorSearch";
import Filters from "./components/Filters";
import Footer from "./components/Footer";
import Header from "./components/Header";

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
    "usa",
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
  const didMount = useRef(false);
  const [query, setQuery] = useState({
    descriptors: [],
    filters: {
      "Exclude Notes/Accords": [],
      "Country of Origin": [],
      Brand: [],
      Gender: [],
      Rating: 1,
    },
  });

  useEffect(() => {
    fetch(`${API_URL}/filters`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setAllNotes(data["notes"].map((x) => x.name));
        setAllAccords(data["accords"].map((x) => x.name));
        setAllCountries(data["countries"].map((x) => x.name));
        setAllBrands(data["brands"].map((x) => x.name));
        setDescriptors(data["descriptors"]);
      });
  }, []);

  useEffect(() => {
    if (!didMount.current) {
      didMount.current = true;
      return;
    }

    console.log(query);
  }, [query]);

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <DescriptorSearch
        descriptors={descriptors}
        setQuery={setQuery}
        currQuery={query}
      />
      <Filters
        descriptors={descriptors}
        accords={allAccords}
        notes={allNotes}
        brands={allBrands}
        countries={allCountries}
        setQuery={setQuery}
        currQuery={query}
      />
      <Footer />
    </div>
  );
}

export default App;

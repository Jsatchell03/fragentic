import { useState, useEffect, useRef } from "react";
import DescriptorSearch from "./components/DescriptorSearch";
import Filters from "./components/Filters";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Results from "./components/Results";

function App() {
  const API_URL = import.meta.env.VITE_BACKEND_URL;
  const [allNotes, setAllNotes] = useState([]);
  const [allAccords, setAllAccords] = useState([]);
  const [allCountries, setAllCountries] = useState([]);
  const [allBrands, setAllBrands] = useState([]);
  const [descriptors, setDescriptors] = useState(allAccords.concat(allNotes));
  const [advancedSearch, setAdvancedSearch] = useState(false);
  const [searchResult, setSearchResult] = useState([]);
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
        setAllNotes(data["notes"]);
        setAllAccords(data["accords"]);
        setAllCountries(data["countries"]);
        setAllBrands(data["brands"]);
        setDescriptors(data["descriptors"]);
      });
  }, []);

  useEffect(() => {
    console.log(query);
    fetch(`${API_URL}/search`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(query),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
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
      <Results />
      <Footer />
    </div>
  );
}

export default App;

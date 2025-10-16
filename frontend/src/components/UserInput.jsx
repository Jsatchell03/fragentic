import { useState, useEffect, useRef } from "react";
import DescriptorSearch from "./DescriptorSearch";
import Filters from "./Filters";
import Results from "./Results";
import Footer from "./Footer";

function UserInput() {
  const API_URL = import.meta.env.VITE_BACKEND_URL;

  const [allNotes, setAllNotes] = useState([]);
  const [allAccords, setAllAccords] = useState([]);
  const [allCountries, setAllCountries] = useState([]);
  const [allBrands, setAllBrands] = useState([]);
  const [descriptors, setDescriptors] = useState([]);
  const [results, setResults] = useState([]);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [query, setQuery] = useState({
    descriptors: [],
    filters: {
      "Exclude Notes/Accords": [],
      "Country of Origin": [],
      Brand: [],
      Gender: [],
      Popularity: [],
      PopularityRange: [],
      Rating: 1,
    },
  });

  const [selectedFilters, setSelectedFilters] = useState(query.filters);
  const [selectedDescriptors, setSelectedDescriptors] = useState([]);

  const filtersRef = useRef(null);
  const [filtersHeight, setFiltersHeight] = useState(0);

  const updateQuery = (queryUpdate, origin) => {
    let newQuery = queryUpdate;
    if (origin === "descriptors") {
      newQuery.filters = selectedFilters;
    } else {
      newQuery.descriptors = selectedDescriptors;
    }
    if (JSON.stringify(newQuery) !== JSON.stringify(query)) {
      setQuery(newQuery);
    } else {
      console.log("Query unchanged, no request sent");
    }
  };

  useEffect(() => {
    fetch(`${API_URL}/filters`)
      .then((res) => res.json())
      .then((data) => {
        setAllNotes(data.notes);
        setAllAccords(data.accords);
        setAllCountries(data.countries);
        setAllBrands(data.brands);
        setDescriptors(data.descriptors);
      });
  }, []);

  const didMount = useRef(false);

  useEffect(() => {
    if (!didMount.current) {
      didMount.current = true;
      return;
    }
    if (query["descriptors"].length > 0) {
      fetch(`${API_URL}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(query),
      })
        .then((res) => res.json())
        .then((data) => setResults(data.results))
        .catch((err) => console.error("Error:", err));
    }
  }, [query]);

  useEffect(() => {
    if (filtersRef.current) {
      setFiltersHeight(filtersRef.current.offsetHeight);
    }
  }, [selectedFilters]);

  return (
    <>
      <DescriptorSearch
        descriptors={descriptors}
        updateQuery={(val) => updateQuery(val, "descriptors")}
        currQuery={query}
        selectedDescriptors={selectedDescriptors}
        setSelectedDescriptors={setSelectedDescriptors}
      />

      <div className="flex items-start space-x-6 mb-5">
        <div ref={filtersRef} className="flex-shrink-0">
          <Filters
            descriptors={descriptors}
            accords={allAccords}
            notes={allNotes}
            brands={allBrands}
            countries={allCountries}
            updateQuery={(val) => updateQuery(val, "filters")}
            selectedFilters={selectedFilters}
            setSelectedFilters={setSelectedFilters}
            currQuery={query}
          />
        </div>
        <div
          className="flex-1 overflow-y-auto overflow-x-hidden"
          style={{ maxHeight: Math.max(filtersHeight, 0) }}
        >
          <Results results={results} />
        </div>
      </div>

      <Footer />
    </>
  );
}

export default UserInput;

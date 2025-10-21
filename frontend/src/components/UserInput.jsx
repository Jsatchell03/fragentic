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

  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

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
    if (filtersRef.current && windowWidth >= 750) {
      setFiltersHeight(filtersRef.current.offsetHeight);
    } else {
      setFiltersHeight(0);
    }
  }, [selectedFilters, filtersOpen, windowWidth]);

  return (
    <div className="w-full flex flex-col min-h-screen">
      <DescriptorSearch
        descriptors={descriptors}
        updateQuery={(val) => updateQuery(val, "descriptors")}
        currQuery={query}
        selectedDescriptors={selectedDescriptors}
        setSelectedDescriptors={setSelectedDescriptors}
      />

      {/* Mobile filter toggle button */}
      <div
        onClick={() => setFiltersOpen(!filtersOpen)}
        className="fat:hidden mx-4 bg-white px-4 py-4 rounded-xl mb-4 shadow-md flex items-center justify-between cursor-pointer"
      >
        <h2 className="font-semibold">
          {filtersOpen ? "Close Filters" : "Add Filters"}
        </h2>
        <div className="w-8">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            className={`transform transition-transform ${
              filtersOpen ? "rotate-180" : ""
            }`}
          >
            <path
              d="M12.7071 14.7071C12.3166 15.0976 11.6834 15.0976 11.2929 14.7071L6.29289 9.70711C5.90237 9.31658 5.90237 8.68342 6.29289 8.29289C6.68342 7.90237 7.31658 7.90237 7.70711 8.29289L12 12.5858L16.2929 8.29289C16.6834 7.90237 17.3166 7.90237 17.7071 8.29289C18.0976 8.68342 18.0976 9.31658 17.7071 9.70711L12.7071 14.7071Z"
              fill="#000000"
            />
          </svg>
        </div>
      </div>

      {/* Main content area - flex-grow to fill available space */}
      <div className="flex flex-col fat:flex-row fat:items-start gap-4 px-4 pb-4 flex-grow overflow-hidden mb-4">
        {/* Filters sidebar - show/hide on mobile based on filtersOpen */}
        <div
          ref={filtersRef}
          className={`${
            filtersOpen ? "block" : "hidden"
          } fat:block w-full fat:w-64 flex-shrink-0 fat:h-auto`}
        >
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

        {/* Results area - scrollable, matches filter height on desktop */}
        <div
          className="flex-1 w-full fat:overflow-y-auto overflow-hidden"
          style={{
            maxHeight: filtersHeight > 0 ? `${filtersHeight}px` : "none",
          }}
        >
          <Results results={results} />
        </div>
      </div>

      <Footer />
    </div>
  );
}

export default UserInput;

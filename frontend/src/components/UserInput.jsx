import { useState, useEffect, useRef } from "react";
import DescriptorSearch from "./DescriptorSearch";
import Filters from "./Filters";
import Results from "./Results";

function UserInput() {
  const API_URL = import.meta.env.VITE_BACKEND_URL;
  const [allNotes, setAllNotes] = useState([]);
  const [allAccords, setAllAccords] = useState([]);
  const [allCountries, setAllCountries] = useState([]);
  const [allBrands, setAllBrands] = useState([]);
  const [descriptors, setDescriptors] = useState(allAccords.concat(allNotes));
  const [advancedSearch, setAdvancedSearch] = useState(false);
  const [results, setResults] = useState([]);

  const didMount = useRef(false);
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
  const [selectedFilters, setSelectedFilters] = useState(query["filters"]);
  const [selectedDescriptors, setSelectedDescriptors] = useState(
    query[descriptors]
  );

  const updateQuery = (queryUpdate, origin) => {
    let newQuery = queryUpdate;
    if (origin == "descriptors") {
      newQuery["filters"] = selectedFilters;
    } else {
      newQuery["descriptors"] = selectedDescriptors;
    }
    setQuery(newQuery);
  };

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
        console.log("Success:", data["results"]);
        setResults(data["results"]);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [query]);

  return (
    <>
      {/* <DescriptorSearch
        descriptors={descriptors}
        updateQuery={(val) => updateQuery(val, "descriptors")}
        currQuery={query}
        selectedDescriptors={selectedDescriptors}
        setSelectedDescriptors={setSelectedDescriptors}
      />
      <div className="flex min-h-screen flex-row space-x-6">
        <div className="overflow-y-auto">
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

        <div className="flex-1 overflow-y-auto">
          <Results results={results} />
        </div>
      </div> */}
      <DescriptorSearch
        descriptors={descriptors}
        updateQuery={(val) => updateQuery(val, "descriptors")}
        currQuery={query}
        selectedDescriptors={selectedDescriptors}
        setSelectedDescriptors={setSelectedDescriptors}
      />
      {/* <div className="flex h-screen overflow-hidden space-x-6">
        <div className="flex-shrink-0">
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

        <div className="flex-1 overflow-y-auto">
          <Results results={results} />
        </div>
      </div> */}

      <div className="flex items-start space-x-6 h-[calc(100vh+3rem)]">
        {/* Filters Sidebar */}
        <div className="flex-shrink-0">
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

        {/* Results Panel */}
        <div className="flex-1 overflow-y-auto h-full">
          <Results results={results} />
        </div>
      </div>
    </>
  );
}

export default UserInput;

import { useState, useEffect, useRef } from "react";
import Header from "./components/Header";
import DescriptorSearch from "./components/DescriptorSearch";
import Filters from "./components/Filters";
import Results from "./components/Results";
import Footer from "./components/Footer";

function App() {
  const [query, setQuery] = useState({
    descriptors: null,
    brands: null,
    countries: null,
    popularity: null,
    rating: null,
  });

  const { descriptors, ...queryFilters } = query;

  const updateDescriptors = (newDescriptors) => {
    setQuery({ ...query, descriptors: newDescriptors });
  };
  console.log(query);

  const updateFilters = (newFilters) => {};

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />
      <main className="flex-grow w-full">
        <DescriptorSearch
          queryDescriptors={query.descriptors}
          updateQuery={updateDescriptors}
        />
        {/* <Filters queryFilters={queryFilters} updateQuery={updateFilters} /> */}
        {/* <Results/> */}
      </main>
      <Footer />
    </div>
  );
}

export default App;

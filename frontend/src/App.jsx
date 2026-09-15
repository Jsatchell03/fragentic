import { useState, useRef, useCallback, memo } from "react";
import Header from "./components/Header";
import DescriptorSearch from "./components/DescriptorSearch";
import Filters from "./components/Filters";
import Results from "./components/Results";
import Footer from "./components/Footer";
import { searchByDescriptors, searchByVector, transformFragrance } from "./api";

const emptyQuery = {
  descriptors: [],
  genders: [],
  brands: [],
  countries: [],
  popularity: [],
  excludedDescriptors: [],
  rating: 0,
};

const arrEq = (a, b) => {
  if (a.length !== b.length) return false;
  const s1 = [...a].sort();
  const s2 = [...b].sort();
  return s1.every((v, i) => v === s2[i]);
};

const filtersEqual = (q1, q2) =>
  arrEq(q1.genders, q2.genders) &&
  arrEq(q1.brands, q2.brands) &&
  arrEq(q1.countries, q2.countries) &&
  arrEq(q1.popularity, q2.popularity) &&
  arrEq(q1.excludedDescriptors, q2.excludedDescriptors) &&
  q1.rating === q2.rating;

const GENDER_MAP = { "For Men": "men", "For Women": "women", Unisex: "unisex" };

function applyClientFilters(fragrances, query) {
  if (!query.genders.length) return fragrances;
  const allowed = new Set(query.genders.map((g) => GENDER_MAP[g]));
  return fragrances.filter((f) => allowed.has(f.gender));
}

const MemoDescriptorSearch = memo(DescriptorSearch);

function App() {
  const currQueryRef = useRef({ ...emptyQuery });
  const lastQueryRef = useRef({ ...emptyQuery });
  const searchVectorRef = useRef(null);
  const [searchActive, setSearchActive] = useState(false);
  const [filtersActive, setFiltersActive] = useState(false);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const updateCurrQuery = (changes) => {
    currQueryRef.current = { ...currQueryRef.current, ...changes };
    if (changes.descriptors?.length === 0) {
      searchVectorRef.current = null;
    }
    const descChanged = !arrEq(
      currQueryRef.current.descriptors,
      lastQueryRef.current.descriptors,
    );
    const filterChanged = !filtersEqual(
      currQueryRef.current,
      lastQueryRef.current,
    );
    if (descChanged !== searchActive) setSearchActive(descChanged);
    if (filterChanged !== filtersActive) setFiltersActive(filterChanged);
  };

  const executeSearch = useCallback(async () => {
    lastQueryRef.current = structuredClone(currQueryRef.current);
    setSearchActive(false);
    setFiltersActive(false);
    if (lastQueryRef.current.descriptors.length === 0) {
      setResults([]);
      return;
    }
    setLoading(true);
    try {
      const data = await searchByDescriptors(lastQueryRef.current);
      searchVectorRef.current = data.search_vector;
      const filtered = applyClientFilters(
        data.fragrances,
        lastQueryRef.current,
      );
      setResults(filtered.map(transformFragrance));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  const executeFilters = useCallback(async () => {
    const prevDescriptors = lastQueryRef.current.descriptors;
    lastQueryRef.current = {
      ...currQueryRef.current,
      descriptors: prevDescriptors,
    };
    setFiltersActive(false);
    if (prevDescriptors.length === 0) return;
    setLoading(true);
    try {
      const data = searchVectorRef.current
        ? await searchByVector(searchVectorRef.current, lastQueryRef.current)
        : await searchByDescriptors(lastQueryRef.current);
      if (data.search_vector) searchVectorRef.current = data.search_vector;
      const filtered = applyClientFilters(
        data.fragrances,
        lastQueryRef.current,
      );
      setResults(filtered.map(transformFragrance));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  const { descriptors, ...initialFilters } = currQueryRef.current;

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Header />
      <main className="flex-1 p-4 flex flex-col gap-4">
        <MemoDescriptorSearch
          initialDescriptors={descriptors}
          searchActive={searchActive}
          updateCurrQuery={updateCurrQuery}
          executeSearch={executeSearch}
        />
        <div className="flex flex-col md:flex-row gap-4 mx-5">
          <div className="md:w-1/4 md:flex-shrink-0">
            <Filters
              initialFilters={initialFilters}
              filtersActive={filtersActive}
              updateCurrQuery={updateCurrQuery}
              executeFilters={executeFilters}
            />
          </div>
          <div className="flex-1 md:relative">
            <div className="md:absolute md:inset-0 md:overflow-hidden">
              <Results results={results} loading={loading} />
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;

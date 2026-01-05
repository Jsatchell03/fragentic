import React, { useState } from "react";
import FragranceCard from "./FragranceCard";
import LoadingSpinner from "./LoadingSpinner";
export default function Results({ results, loading = true }) {
  const [sortOption, setSortOption] = useState("relevance-desc");
  const [limit, setLimit] = useState(20);

  const sortedResults = [...results].sort((a, b) => {
    switch (sortOption) {
      case "rating-asc":
        return a.rating - b.rating;
      case "rating-desc":
        return b.rating - a.rating;
      case "popularity-asc":
        return a.popularity - b.popularity;
      case "popularity-desc":
        return b.popularity - a.popularity;
      case "relevance-desc":
        return b.score - a.score;
      default:
        return 0;
    }
  });

  const limitedResults = sortedResults.slice(0, limit);
  if (loading) {
    return (
      <div className="w-full h-full flex items-center justify-center overflow-hidden">
        <div className="w-1/2">
          <LoadingSpinner />
        </div>
      </div>
    );
  }
  if (results.length === 0) {
    return null;
  }

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-shrink-0 flex flex-row justify-between items-center gap-2 sm:gap-4 mb-4 bg-white p-2 sm:p-4 rounded-xl shadow-md sticky top-0 z-10">
        <div className="flex items-center space-x-1 sm:space-x-3 min-w-0">
          <label
            htmlFor="limit"
            className="text-gray-600 text-xs sm:text-sm whitespace-nowrap"
          >
            Results: {limit}
          </label>
          <input
            id="limit"
            type="range"
            min="5"
            max="100"
            step="5"
            value={limit}
            onChange={(e) => setLimit(parseInt(e.target.value))}
            className="w-20 sm:w-32 lg:w-40 accent-purple-500 cursor-pointer flex-shrink-0"
          />
        </div>

        <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
          <label
            htmlFor="sort"
            className="text-gray-600 text-xs sm:text-sm whitespace-nowrap"
          >
            Sort:
          </label>
          <select
            id="sort"
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
            className="border border-purple-600 rounded-md text-xs sm:text-sm p-1 sm:p-2 focus:outline-none bg-white"
          >
            <option value="relevance-desc">Relevance</option>
            <option value="rating-desc">Highest Rated</option>
            <option value="rating-asc">Lowest Rated</option>
            <option value="popularity-desc">Most Popular</option>
            <option value="popularity-asc">Least Popular</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 py-5">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {limitedResults.map((fragrance, idx) => (
            <FragranceCard key={idx} fragrance={fragrance} />
          ))}
        </div>
      </div>
    </div>
  );
}

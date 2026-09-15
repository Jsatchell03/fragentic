import React, { useState } from "react";
import FragranceCard from "./FragranceCard";
import LoadingSpinner from "./LoadingSpinner";
export default function Results({ results, loading = true }) {
  const [sortOption, setSortOption] = useState("relevance-desc");

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
    return (
      <div className="w-full h-full flex items-center justify-center">
        <p className="text-gray-400 text-lg">Search for fragrances above</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-shrink-0 flex flex-row justify-end items-center gap-1 mb-1 px-1 py-0.5 sticky top-0 z-10">
        <div className="flex items-center gap-1 flex-shrink-0">
          <label
            htmlFor="sort"
            className="text-gray-600 text-xs whitespace-nowrap"
          >
            Sort:
          </label>
          <select
            id="sort"
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
            className="border border-purple-600 rounded text-xs p-0.5 focus:outline-none bg-white"
          >
            <option value="relevance-desc">Relevance</option>
            <option value="rating-desc">Highest Rated</option>
            <option value="rating-asc">Lowest Rated</option>
            <option value="popularity-desc">Most Popular</option>
            <option value="popularity-asc">Least Popular</option>
          </select>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2">
        <div className="pb-2 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {sortedResults.map((fragrance, idx) => (
            <FragranceCard key={idx} fragrance={fragrance} />
          ))}
        </div>
      </div>
    </div>
  );
}

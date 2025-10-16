import React, { useState } from "react";
import FragranceCard from "./FragranceCard";

export default function Results({ results }) {
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
  return (
    <div className="mr-4 flex-1">
      <div className="flex justify-between items-center mb-4 pr-2">
        <div className="flex items-center space-x-3">
          <label htmlFor="limit" className="text-gray-600 text-sm">
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
            className="w-40 accent-purple-500 cursor-pointer"
          />
        </div>

        <div className="flex items-center">
          <label htmlFor="sort" className="text-gray-600 text-sm mr-2">
            Sort:
          </label>
          <select
            id="sort"
            value={sortOption}
            onChange={(e) => setSortOption(e.target.value)}
            className="border border-purple-600 rounded-md text-sm p-2 focus:outline-none"
          >
            <option value="relevance-desc">Relevance</option>
            <option value="rating-desc">Highest Rated</option>
            <option value="rating-asc">Lowest Rated</option>
            <option value="popularity-desc">Most Popular</option>
            <option value="popularity-asc">Least Popular</option>
          </select>
        </div>
      </div>

      {/* Results grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 overflow-y-auto pr-2">
        {limitedResults.map((fragrance, idx) => (
          <FragranceCard key={idx} fragrance={fragrance} />
        ))}
      </div>
    </div>
  );
}

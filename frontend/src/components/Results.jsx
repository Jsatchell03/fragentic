import React from "react";
import FragranceCard from "./FragranceCard";

export default function Results({ results }) {
  return (
    <div className="mr-4 flex-1">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {results.map((fragrance, idx) => (
          <FragranceCard key={idx} fragrance={fragrance} />
        ))}
      </div>
    </div>
  );
}

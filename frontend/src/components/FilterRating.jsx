import { useState } from "react";
import React from "react";

export default function FilterRating({ title, currFilters, setCurrFilters }) {
  const maxStars = 4;
  const [rating, setRating] = useState(currFilters[title] || 1);
  const [hover, setHover] = useState(0); // for hover effect

  const handleClick = (value) => {
    setRating(value);
    setCurrFilters({ ...currFilters, [title]: value });
  };

  return (
    <>
      <p className="font-medium mb-2 text-gray-700">{title}</p>
      <div className="">
        <div className="mb-2">
          <div className="flex space-x-1 mb-0">
            {Array.from({ length: maxStars }, (_, i) => i + 1).map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => handleClick(star)}
                onMouseEnter={() => setHover(star)}
                onMouseLeave={() => setHover(0)}
                className="focus:outline-none"
              >
                <svg
                  className={`w-6 h-6 ${
                    star <= (hover || rating)
                      ? "text-yellow-400"
                      : "text-gray-300"
                  }`}
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.946a1 1 0 00.95.69h4.15c.969 0 1.371 1.24.588 1.81l-3.36 2.44a1 1 0 00-.364 1.118l1.287 3.945c.3.921-.755 1.688-1.54 1.118l-3.36-2.44a1 1 0 00-1.176 0l-3.36 2.44c-.784.57-1.838-.197-1.539-1.118l1.287-3.945a1 1 0 00-.364-1.118L2.034 9.373c-.783-.57-.38-1.81.588-1.81h4.15a1 1 0 00.95-.69l1.286-3.946z" />
                </svg>
              </button>
            ))}
          </div>
        </div>
        <p>{rating} star(s) & up</p>
      </div>
    </>
  );
}

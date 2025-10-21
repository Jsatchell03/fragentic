import React from "react";

export default function FragranceCard({ fragrance }) {
  const { name, brand, rating, descriptors, url, gender, score } = fragrance;

  const displayedDescriptors = descriptors.slice(0, 15);

  function capitalizeBrand(name) {
    return name
      .split("-")
      .map((word) => word[0].toUpperCase() + word.slice(1))
      .join(" ");
  }

  function capitalizeGender(gender) {
    const firstLetter = gender.charAt(0).toUpperCase();
    const restOfString = gender.slice(1);
    if (gender !== "unisex") {
      return "For " + firstLetter + restOfString;
    } else {
      return firstLetter + restOfString;
    }
  }

  function capitalizeName(name) {
    return name
      .split("-")
      .map((word) => word[0].toUpperCase() + word.slice(1))
      .join(" ");
  }

  return (
    <div className="flex flex-col justify-between bg-white shadow-md rounded-xl p-4 hover:shadow-xl transition-shadow duration-300 h-full">
      <div>
        {/* Name */}
        <div className="mb-1 flex flex-row justify-between items-start gap-2">
          <div className="text-xl font-bold text-gray-800 flex-1">
            {capitalizeName(name)}
          </div>
          <div className="text-xs text-gray-500 whitespace-nowrap">
            {Math.trunc(score * 100) + "% match"}
          </div>
        </div>

        {/* Brand */}
        <div className="flex flex-row justify-between mb-4">
          <div className="text-gray-500">By {capitalizeBrand(brand)}</div>
          <div className="text-gray-500 ">{capitalizeGender(gender)}</div>
        </div>

        {/* Descriptors */}
        <div className="flex flex-wrap gap-2">
          {displayedDescriptors.map((desc, idx) => (
            <span
              key={idx}
              className="bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-sm"
            >
              {desc}
            </span>
          ))}
        </div>
      </div>

      {/* Footer section */}
      <div className="mt-4 flex items-center justify-between">
        <div>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-gray-800 hover:text-purple-600 transition-colors"
          >
            <span className="text-gray-500">More Info</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-3 w-3"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path d="M20.2929 9.70708C20.5789 9.99307 21.009 10.0786 21.3827 9.92385C21.7564 9.76907 22 9.40443 22 8.99997V2.99997C22 2.44768 21.5523 1.99997 21 1.99997H15C14.5955 1.99997 14.2309 2.24361 14.0761 2.61729C13.9213 2.99096 14.0069 3.42108 14.2929 3.70708L16.2322 5.64641L9.58574 12.2929C9.19522 12.6834 9.19522 13.3166 9.58574 13.7071L10.2928 14.4142C10.6834 14.8048 11.3165 14.8048 11.7071 14.4142L18.3536 7.76774L20.2929 9.70708Z" />
              <path d="M4.5 8.00006C4.5 7.72392 4.72386 7.50006 5 7.50006H10.0625C10.6148 7.50006 11.0625 7.05234 11.0625 6.50006V5.50006C11.0625 4.94777 10.6148 4.50006 10.0625 4.50006H5C3.067 4.50006 1.5 6.06706 1.5 8.00006V19.0001C1.5 20.9331 3.067 22.5001 5 22.5001H16C17.933 22.5001 19.5 20.9331 19.5 19.0001V13.9376C19.5 13.3853 19.0523 12.9376 18.5 12.9376H17.5C16.9477 12.9376 16.5 13.3853 16.5 13.9376V19.0001C16.5 19.2762 16.2761 19.5001 16 19.5001H5C4.72386 19.5001 4.5 19.2762 4.5 19.0001V8.00006Z" />
            </svg>
          </a>
        </div>

        {/* Rating with single star */}
        <div className="flex items-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 text-yellow-400"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.946a1 1 0 00.95.69h4.15c.969 0 1.371 1.24.588 1.81l-3.36 2.44a1 1 0 00-.364 1.118l1.287 3.945c.3.921-.755 1.688-1.54 1.118l-3.36-2.44a1 1 0 00-1.176 0l-3.36 2.44c-.784.57-1.838-.197-1.539-1.118l1.287-3.945a1 1 0 00-.364-1.118L2.034 9.373c-.783-.57-.38-1.81.588-1.81h4.15a1 1 0 00.95-.69l1.286-3.946z" />
          </svg>
          <span className="ml-2 text-gray-600 font-medium">
            {rating.toFixed(1)}
          </span>
        </div>
      </div>
    </div>
  );
}

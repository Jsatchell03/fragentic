import React from "react";

export default function BuyOnAmazon({ name, brand, gender }) {
  const AMAZON_ASSOCIATE_TAG = import.meta.env.VITE_AMAZON_ASSOCIATE_TAG;
  let genderSearch = gender.replaceAll(" ", "+");
  let amazonLink =
    "https://www.amazon.com/s?k=" +
    name +
    "+" +
    brand +
    (gender === "For Women" ? "+ Perfume" : "+ Cologne") +
    "+" +
    genderSearch +
    AMAZON_ASSOCIATE_TAG;
  return (
    <>
      <a href={amazonLink} target="_blank">
        <div className="mt-4 w-full flex items-center justify-center p-2 border border-yellow-400 bg-yellow-100 rounded-lg hover:bg-yellow-200 transition-colors cursor-pointer">
          <p>Buy On</p>
          <img
            src="https://www.vectorlogo.zone/logos/amazon/amazon-ar21.svg"
            alt="Amazon logo"
          />
        </div>
      </a>
    </>
  );
}

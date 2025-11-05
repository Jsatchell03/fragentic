import React from "react";

export default function LoadingSpinner({
  color = "border-purple-600",
  thickness = "border-24",
  text = "Loading...",
}) {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full gap-4 my-4">
      <div
        className={`w-3/4 aspect-square ${thickness} ${color} border-t-transparent rounded-full animate-spin`}
      />
      <p className="text-lg">{text}</p>
    </div>
  );
}

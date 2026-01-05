import { useState, useEffect, useRef } from "react";
import Header from "./components/Header";
import UserInput from "./components/UserInput";
import BuyOnAmazon from "./components/BuyOnAmazon";
function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />
      <main className="flex-grow w-full">
        <UserInput />
      </main>
    </div>
  );
}

export default App;

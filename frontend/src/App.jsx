import { useState, useEffect, useRef } from "react";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Results from "./components/Results";

import UserInput from "./components/UserInput";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <UserInput />
      <Footer />
    </div>
  );
}

export default App;

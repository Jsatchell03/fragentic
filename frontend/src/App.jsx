import { useState, useEffect, useRef } from "react";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Results from "./components/Results";

import UserInput from "./components/UserInput";

function App() {
  return (
    // <div className="flex flex-col bg-gray-100">
    //   <Header />

    //   {/* This grows to fill the available vertical space */}
    //   <main className="flex-grow">
    //     <UserInput />
    //   </main>

    //   <Footer />
    // </div>

    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />

      {/* let main grow and allow visible overflow so a tall UserInput pushes footer down */}
      <main className="flex-grow overflow-visible">
        <UserInput />
      </main>
    </div>
    // div className="min-h-screen bg-gray-100">
    //   <Header />
    //   <UserInput />
    //   <Footer />
    // </div>
  );
}

export default App;

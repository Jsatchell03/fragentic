// components/Footer.jsx
export default function Footer() {
  return (
    //
    <footer className="bg-footer text-gray-200 py-4 mt-5">
      <div className="w-full pl-4 flex justify-between items-center">
        <div className="w-64 text-xs/3 sm:w-132 sm:text-sm/4">
          <p>
            Questions? Feature suggestions? Let us know! We would love to make
            this site more useful. Hit the "Contact Us" button and let us know
            about any bugs, or features you would like to see on Fragentic.
          </p>
        </div>
        <div className="flex flex-col justify-between w-32 sm:w-64 items-center">
          <div className="ml-4 text-xs w-32">
            <a
              href="#contact" // link to contact section or page
              className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-xl transition-colors sm:text-[16px] sm:px-4 py-2"
            >
              Contact Us
            </a>
          </div>
          <div className="mt-4 md:mb-0 text-center md:text-left">
            <p className="text-xs text-gray-400">
              © {new Date().getFullYear()} Fragentic
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

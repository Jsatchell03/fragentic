export default function Footer() {
  return (
    <footer className="bg-footer text-gray-200 py-6 mt-2 w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          {/* Left section - description */}
          <div className="max-w-md text-center sm:text-left">
            <p className="text-sm leading-relaxed">
              Questions? Feature suggestions? Let us know! We would love to make
              this site more useful. Hit the "Contact Us" button and let us know
              about any bugs, or features you would like to see on Fragentic.
            </p>
          </div>

          {/* Right section - button and copyright */}
          <div className="flex flex-col items-center gap-3">
            <a
              href="#contact"
              className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-xl transition-colors"
            >
              Contact Us
            </a>
            <p className="text-xs text-gray-400">
              © {new Date().getFullYear()} Fragentic
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

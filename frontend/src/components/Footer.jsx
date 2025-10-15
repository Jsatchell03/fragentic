// components/Footer.jsx
export default function Footer() {
  return (
    <footer className="bg-footer text-gray-200 py-6 mt-5">
      <div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
        {/* Made by */}
        <div className="mb-4 md:mb-0 text-center md:text-left">
          <p className="text-sm text-gray-400">
            © {new Date().getFullYear()} Fragentic
          </p>
        </div>
      </div>
    </footer>
  );
}

import { useState, useEffect } from "react";

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed w-full top-0 z-50 transition-shadow px-6 py-4 ${
        scrolled ? "shadow-lg bg-blue-700" : "bg-blue-700"
      } text-white`}
    >
      <ul className="flex justify-center gap-8 font-semibold">
        <li><a href="#home" className="hover:text-gray-200">Home</a></li>
        <li><a href="#about" className="hover:text-gray-200">About</a></li>
        <li><a href="#how" className="hover:text-gray-200">How It Works</a></li>
        <li><a href="#upload" className="hover:text-gray-200">Upload</a></li>
        <li><a href="#author" className="hover:text-gray-200">Author</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;

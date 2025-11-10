const AuthorInfo = () => (
  <section
    id="author"
    className="py-16 px-6 bg-gray-100 flex justify-center"
  >
    <div className="max-w-3xl flex flex-col items-center gap-4 text-center">

      {/* Author Info */}
      <h2 className="text-3xl font-bold">Mukesh Kumar Mahato</h2>
      <p className="text-lg font-semibold text-gray-700">AI Researcher & Developer</p>
      <p className="text-gray-600">
        Building intelligent healthcare systems using deep learning, computer vision, and cloud deployment.
      </p>
      <p className="text-gray-600 font-medium">
        🎓 College: The Kyoto College of Graduate Studies for Informatics (KCGI)
      </p>

      {/* Social Links with Icons */}
      <div className="flex justify-center gap-6 mt-4">

        {/* LinkedIn */}
        <a
          href="https://www.linkedin.com/in/your-linkedin-id"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium transition"
        >
          {/* LinkedIn SVG */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.762 2.239 5 5 5h14c2.762 0 5-2.238 5-5v-14c0-2.761-2.238-5-5-5zm-11.667 20h-3.333v-11h3.333v11zm-1.667-12.259c-1.067 0-1.933-.867-1.933-1.941 0-1.073.867-1.938 1.933-1.938s1.933.865 1.933 1.938c0 1.074-.867 1.941-1.933 1.941zm13.334 12.259h-3.334v-5.667c0-1.352-.027-3.093-1.887-3.093-1.887 0-2.177 1.476-2.177 3v5.76h-3.333v-11h3.201v1.507h.045c.446-.844 1.537-1.733 3.164-1.733 3.381 0 4.003 2.225 4.003 5.117v6.109z"/>
          </svg>
          LinkedIn
        </a>

        {/* Resume / Website */}
        <a
          href="https://your-resume-site.com"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 text-green-600 hover:text-green-800 font-medium transition"
        >
          {/* Document / Resume SVG */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-5 h-5"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M6 2C4.9 2 4 2.9 4 4v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6H6zm7 1.5L18.5 9H13V3.5z"/>
          </svg>
          Resume
        </a>

      </div>

    </div>
  </section>
);

export default AuthorInfo;

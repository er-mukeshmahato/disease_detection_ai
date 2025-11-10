const HowItWorks = () => (
  <section id="how" className="py-16 px-6 bg-gray-100 text-center">
    <h2 className="text-3xl font-bold mb-6">How It Works</h2>
    <div className="max-w-4xl mx-auto grid md:grid-cols-3 gap-8">
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-semibold text-xl mb-2">1️⃣ Upload</h3>
        <p>Upload your chest X-ray image in PNG or JPG format.</p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-semibold text-xl mb-2">2️⃣ Analyze</h3>
        <p>The AI model processes and extracts image features using CNN layers.</p>
      </div>
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="font-semibold text-xl mb-2">3️⃣ Predict</h3>
        <p>The system outputs the most likely disease category with confidence.</p>
      </div>
    </div>
  </section>
);

export default HowItWorks;

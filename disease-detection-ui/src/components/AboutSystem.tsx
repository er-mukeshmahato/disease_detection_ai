const AboutSystem = () => (
  <section id="about" className="py-16 px-6 bg-white text-center">
    <h2 className="text-3xl font-bold mb-6">About the System</h2>
    <p className="max-w-3xl mx-auto text-gray-700 leading-relaxed">
      This system uses a convolutional neural network (CNN) trained on labeled X-ray images to classify lung-related diseases. 
      The model predicts the probability of conditions like Pneumonia, COVID-19 and Tuberculosis by analyzing 
      visual patterns and textures invisible to the human eye.
    </p>
  </section>
);

export default AboutSystem;

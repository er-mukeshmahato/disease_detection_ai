import Navbar from "./components/navbar";
import HeroSection from "./components/HeroSection";
import AboutSystem from "./components/AboutSystem";
import HowItWorks from "./components/HowItWorks";
import UploadSection from "./components/UploadSection";
import AuthorInfo from "./components/AuthorInfo";
import Footer from "./components/Footer";

const App = () => (
  <div>
    <Navbar />
    <main className="pt-20">
      <HeroSection />
      <AboutSystem />
      <HowItWorks />
      <UploadSection />
      <AuthorInfo />
    </main>
    <Footer />
  </div>
);

export default App;

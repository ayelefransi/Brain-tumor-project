import React from "react";
import EnhancedHeroSection from "../components/enhanced/EnhancedHeroSection";
import AboutPart from "../components/AboutPart/AboutPart";
import Values from "../components/Values/Values";
import BackToTopButton from "../components/BackToTop/BackToTop";
import Footer from "../components/Footer/Footer";

function EnhancedHome() {
  return (
    <>
      <EnhancedHeroSection />
      <AboutPart />
      <Values />
      <BackToTopButton />
      <Footer />
    </>
  );
}

export default EnhancedHome;
import { useState } from "react";
import Header from "./components/Header.jsx";
import Hero from "./components/Hero.jsx";
import AnalyzerCard from "./components/AnalyzerCard.jsx";
import ResultPanel from "./components/ResultPanel.jsx";
import Footer from "./components/Footer.jsx";
import { useHealthCheck } from "./hooks/useHealthCheck.js";

export default function App() {
  const { status } = useHealthCheck();
  const [result, setResult] = useState(null);

  return (
    <div className="min-h-screen bg-white">
      <div className="mx-auto flex min-h-screen max-w-app flex-col px-5">
        <Header status={status} />
        <main className="flex-1">
          <Hero />
          <AnalyzerCard onResult={setResult} />
          {result && <ResultPanel result={result} />}
        </main>
        <Footer />
      </div>
    </div>
  );
}

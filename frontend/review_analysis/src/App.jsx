import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MainPage from "./pages/MainPage";
import ReviewAnalysis from "./pages/ReviewsAnalysis";

function App() {
  return (
     <BrowserRouter>
      {/* <nav style={{ display: "flex", gap: "20px", margin: "20px" }}>
        <Link to="/">Главная</Link>
        <Link to="/analyzer">Анализатор</Link>
      </nav> */}

      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/reviews-analysis" element={<ReviewAnalysis />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

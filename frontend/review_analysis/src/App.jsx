import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MainPage from "./pages/MainPage";
import ReviewAnalysis from "./pages/ReviewsAnalysis";

function App() {
  return (
     <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/reviews-analysis/:id" element={<ReviewAnalysis />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

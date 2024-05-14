import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle";
import AttendanceList from "./components/AttendanceList/AttendanceList";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./components/Home/Home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/attendance" element={<AttendanceList />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

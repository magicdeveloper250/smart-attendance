import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle";
import AttendanceList from "./components/AttendanceList/AttendanceList";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./components/Home/Home";
import SingleAttendance from "./components/SingleAttendance/SingleAttendance";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/attendance" element={<AttendanceList />} />
        <Route path="/attendance/:date" element={<SingleAttendance />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

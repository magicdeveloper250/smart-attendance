import { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AttendanceTable from "../AttendanceTable/AttendanceTable";
import { useReactToPrint } from "react-to-print";
import "./SingleAttendance.css";

function SingleAttendance() {
  const day = useParams().date;
  const navigate = useNavigate();
  const printContentRef = useRef();
  const handlePrint = useReactToPrint({
    content: () => printContentRef.current,
    copyStyles: true,
    removeAfterPrint: true,
  });
  const [dayInfo, setDayInfo] = useState([]);
  useEffect(() => {
    const getAttendance = async () => {
      try {
        const resp = await fetch(
          `${import.meta.env.VITE_SERVER_URL}/attendance/${day}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        const data = await resp.json();
        if (resp.ok) {
          setDayInfo(data.data);
        }
      } catch (error) {
        console.log(String(error));
      }
    };
    getAttendance();
  }, []);

  return (
    <div ref={printContentRef}>
      <header className="single-attendance__header">
        <span>
          <h2 className="h2">Attendance of {day}</h2>{" "}
        </span>
        <span>
          <button className="btn btn-outline-secondary" onClick={handlePrint}>
            Print Report
          </button>
        </span>
      </header>
      <button onClick={() => navigate(-1)} className="btn btn-secondary">
        Back
      </button>
      <main>
        <AttendanceTable data={dayInfo} />
      </main>
    </div>
  );
}

export default SingleAttendance;

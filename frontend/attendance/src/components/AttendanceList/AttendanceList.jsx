import React, { useRef } from "react";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";
import "./AttendanceList.css";
import AttendanceNav from "../AttendanceNav/AttendanceNav";
import TimeSelector from "../TimeSelector/TimeSelector";
import AttendanceTable from "../AttendanceTable/AttendanceTable";

function AttendanceList() {
  const [dayInfo, setDayInfo] = useState([]);
  const timeSelectorEl = useRef();
  const [showHistory, setShowHstory] = useState(false);

  useEffect(() => {
    const connection = io.connect("http://localhost:5000");
    connection.on("connect", () => console.log("✅Connected"));
    connection.on("disconnect", () => console.log("❌Disconnected"));
    connection.on("attend", (data) => {
      setDayInfo(data);
    });
    return () => connection.disconnect();
  }, []);
  useEffect(() => {
    const getToDay = async () => {
      try {
        const resp = await fetch("http://localhost:5000/today", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await resp.json();
        if (resp.ok) {
          setDayInfo(data.day);
        }
      } catch (error) {
        alert(String(error));
      }
    };
    getToDay();
  }, []);
  useEffect(() => {
    const el = timeSelectorEl.current;
    showHistory == false
      ? (el.style.display = "none")
      : (el.style.display = "block");
  }, [showHistory]);
  return (
    <>
      <AttendanceNav
        day={dayInfo.day}
        onHistoryClicked={() => setShowHstory(!showHistory)}
      />
      <TimeSelector
        refer={timeSelectorEl}
        onClose={() => setShowHstory(!showHistory)}
      />
      <AttendanceTable data={dayInfo} />
    </>
  );
}

export default AttendanceList;

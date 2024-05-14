import React from "react";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";

function AttendanceList() {
  const [dayInfo, setDayInfo] = useState([]);

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
  return (
    <>
      <div className="d-flex flex-between">
        <h1>ATTENDANCE SYSTEM</h1> <h5>{dayInfo.day}</h5>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th scope="col">id</th>
            <th scope="col">Regnumber</th>
            <th scope="col">name</th>
            <th scope="col">attended</th>
          </tr>
        </thead>
        <tbody>
          {dayInfo?.attendees?.map((student, index) => {
            return (
              <tr key={index} scope="col">
                <td>{student._id}</td>
                <td>{student.reg}</td>
                <td>{student.name}</td>
                <td>{student.attended ? "✅" : "❌"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}

export default AttendanceList;

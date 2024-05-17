import React, { useRef } from "react";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";
import "./AttendanceList.css";
import AttendanceNav from "../AttendanceNav/AttendanceNav";
import TimeSelector from "../TimeSelector/TimeSelector";
import AttendanceTable from "../AttendanceTable/AttendanceTable";
import AddNewForm from "../AddNewForm/AddNewForm";

function AttendanceList() {
  const [dayInfo, setDayInfo] = useState([]);
  const refs = { historyRef: useRef(), formRef: useRef() };
  const [showDialog, setShowDialog] = useState({
    historyDialog: false,
    formDialog: false,
  });

  useEffect(() => {
    const connection = io.connect(`${import.meta.env.VITE_SERVER_URL}`);
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
        const resp = await fetch(`${import.meta.env.VITE_SERVER_URL}/today`, {
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
    if (showDialog.historyDialog) {
      refs.historyRef.current.style.display = "block";
      refs.formRef.current.style.display = "none";
    } else if (showDialog.formDialog) {
      refs.formRef.current.style.display = "block";
      refs.historyRef.current.style.display = "none";
    } else {
      refs.historyRef.current.style.display = "none";
      refs.formRef.current.style.display = "none";
    }
  }, [showDialog]);
  return (
    <>
      <AttendanceNav
        day={dayInfo.day}
        onHistoryClicked={() =>
          setShowDialog({
            ...showDialog,
            historyDialog: !showDialog.historyDialog,
          })
        }
        onNewClicked={() =>
          setShowDialog({
            ...showDialog,
            formDialog: !showDialog.formDialog,
          })
        }
      />
      <AddNewForm
        refer={refs.formRef}
        onClose={() =>
          setShowDialog({
            ...showDialog,
            formDialog: !showDialog.formDialog,
          })
        }
      />
      <TimeSelector
        refer={refs.historyRef}
        onClose={() =>
          setShowDialog({
            ...showDialog,
            historyDialog: !showDialog.historyDialog,
          })
        }
      />
      <AttendanceTable data={dayInfo} />
    </>
  );
}

export default AttendanceList;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const openDay = async () => {
    try {
      const resp = await fetch("http://localhost:5000/openDay", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      });
      const data = await resp.json();
      if (resp.ok) {
        navigate("/attendance");
      }
    } catch (error) {
      alert(String(error));
    }
  };
  return (
    <div className="d-flex flex-column">
      <h1 className="text-center">Welcome to smart attendance</h1>
      <button className="btn btn-primary btn-lg" onClick={openDay}>
        Take attendance
      </button>
    </div>
  );
}

export default Home;

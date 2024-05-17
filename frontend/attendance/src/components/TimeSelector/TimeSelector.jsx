import { useEffect, useState } from "react";
import "./TimeSelector.css";
import { Link } from "react-router-dom";
function TimeSelector({ refer, onClose }) {
  const [timeStamps, setTimeStamps] = useState([]);
  useEffect(() => {
    const getTimeStamps = async () => {
      try {
        const resp = await fetch(
          `${import.meta.env.VITE_SERVER_URL}/timeStamps`,
          {
            method: "GET",
            headers: {
              Content_Type: "application/json",
            },
          }
        );
        const data = await resp.json();
        if (resp.ok) {
          setTimeStamps(data.data);
        }
      } catch (error) {
        console.log(String(error));
      }
    };
    getTimeStamps();
  }, []);
  return (
    <div className="modal" tabIndex="-1" role="dialog" ref={refer}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <div className="modal-title">
              <h3>Pick Date</h3>
            </div>
            <button
              className="btn btn-outline-secondary btn-close"
              onClick={onClose}
            ></button>
          </div>
          <div className="modal-body">
            <section className="timeStamps-container">
              {timeStamps?.map((timeStamp, index) => {
                return (
                  <Link to={`/attendance/${timeStamp.day}`} key={index}>
                    <button className="btn btn-outline-secondary">
                      {timeStamp.day}
                    </button>
                  </Link>
                );
              })}
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TimeSelector;

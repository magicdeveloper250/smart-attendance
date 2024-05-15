import "./AttendanceNav.css";
function AttendanceNav({ day, onHistoryClicked }) {
  return (
    <nav className="nav">
      <section className="nav__logo">
        <h1 className="h3">SMART ATTENDANCE SYSTEM</h1>
      </section>
      <section className="nav__list">
        <span className="nav__item">
          <button
            className="btn btn-outline-secondary"
            onClick={onHistoryClicked}
          >
            Report
          </button>
        </span>
        <span className="nav__item">
          <h5>{day}</h5>
        </span>
      </section>
    </nav>
  );
}

export default AttendanceNav;

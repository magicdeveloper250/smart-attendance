import "./AttendanceNav.css";
function AttendanceNav({ day, onHistoryClicked, onNewClicked }) {
  return (
    <nav className="nav">
      <section className="nav__logo">
        <h1 className="h3">SMART ATTENDANCE SYSTEM</h1>
      </section>
      <section className="nav__list">
        <button
          className="btn btn-outline-secondary nav__item"
          onClick={onNewClicked}
        >
          New
        </button>
        <button
          className="btn btn-outline-secondary nav__item"
          onClick={onHistoryClicked}
        >
          Report
        </button>

        <span className="nav__item">
          <h5>{day}</h5>
        </span>
      </section>
    </nav>
  );
}

export default AttendanceNav;

function AttendanceTable({ data }) {
  return (
    <table className="table">
      <thead>
        <tr>
          <th scope="col">Regnumber</th>
          <th scope="col">Name</th>
          <th scope="col">Attended</th>
          <th scope="col">Time</th>
        </tr>
      </thead>
      <tbody>
        {data?.attendees?.map((student, index) => {
          return (
            <tr key={index} scope="col">
              <td>{student.reg}</td>
              <td>{student.name}</td>
              <td>{student.attended ? "✅" : "❌"}</td>
              <td>{student.time}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default AttendanceTable;

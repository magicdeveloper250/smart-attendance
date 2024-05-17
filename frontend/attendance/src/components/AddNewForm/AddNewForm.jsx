import React from "react";
import { useState } from "react";
import "./AddNewForm.css";

function AddNewForm({ refer, onClose }) {
  const [newUser, setNewUser] = useState({
    name: "",
    regnumber: "",
    image: "",
  });
  const handleChange = (e) => {
    setNewUser({ ...newUser, [e.target.name]: e.target.value });
  };

  const handleChangeImage = (e) => {
    setNewUser({ ...newUser, [e.target.name]: e.target.files[0] });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", newUser.name);
    formData.append("regnumber", newUser.regnumber);
    formData.append("image", newUser.image);

    // sending data to the server
    try {
      const resp = await fetch(`${import.meta.env.VITE_SERVER_URL}/addNew`, {
        method: "POST",
        headers: {
          encType: "multipart/form-data",
        },
        body: formData,
      });
      const data = await resp.json();
      if (resp.ok) {
        onClose();
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.log(String(error));
    }
  };
  return (
    <div className="modal" tabIndex="-1" role="dialog" ref={refer}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <div className="modal-title">
              <h3>Add new</h3>
            </div>
            <button
              className="btn btn-outline-secondary btn-close"
              onClick={onClose}
            ></button>
          </div>

          <div className="modal-body">
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  required
                  className="form-control"
                  name="name"
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="regnumber">Reg number</label>
                <input
                  type="text"
                  required
                  name="regnumber"
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
              {newUser?.image && (
                <div className="image-preview">
                  <img
                    src={
                      newUser.image ? URL.createObjectURL(newUser.image) : ""
                    }
                    alt={newUser.name}
                    width={"350px"}
                  />
                </div>
              )}
              <div className="form-control">
                <label htmlFor="image">Face Image</label>
                <input
                  type="file"
                  accept=".jpg, .png"
                  required
                  onChange={handleChangeImage}
                  className="form-control"
                  name="image"
                />
              </div>
              <div className="form-group">
                <button className="btn btn-primary" type="submit">
                  Submit
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddNewForm;

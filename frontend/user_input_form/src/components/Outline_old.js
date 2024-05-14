import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";

const Outline = () => {
  const dispatch = useDispatch();
  const description = useSelector((e) => e.description.value);
  
  const [outlines, setOutlines] = useState(description.outline.length > 0 ? description.outline : [""]);

  useEffect(() => {
    dispatch(info({ ...description, outline: outlines }));
  }, [outlines]);

  const addOutline = (index) => {
    const newOutlines = [...outlines];
    newOutlines.splice(index + 1, 0, ""); // 在指定索引后添加一个新的空字符串
    setOutlines(newOutlines);
  };

  const removeOutline = (index) => {
    const newOutlines = outlines.filter((_, idx) => idx !== index);
    setOutlines(newOutlines);
  };

  const handleChange = (index, value) => {
    const newOutlines = [...outlines];
    newOutlines[index] = value;
    setOutlines(newOutlines);
  };

  return (
    <div className="outline">
      {/* <h2>Article Outline</h2> */}
      <div className="outlines-container">
        <label>目录</label>
        {outlines.map((outline, index) => (
          <div key={index} className="outline-item">
            <input
              type="text"
              value={outline}
              onChange={(e) => handleChange(index, e.target.value)}
              className="outline-input"
              placeholder="e.g. 引言"
            />
            {/* Add button with the add-btn class */}
            <button
              type="button"
              className="add-btn"
              onClick={() => addOutline(index)}
            >
              +
            </button>
            {outlines.length > 1 && (
            <button
              type="button"
              className="delete-btn"
              onClick={() => removeOutline(index)}
            >
              ×
            </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Outline;

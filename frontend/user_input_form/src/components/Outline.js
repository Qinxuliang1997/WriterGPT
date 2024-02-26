import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";

const Outline = () => {
  const dispatch = useDispatch();
  const article = useSelector((e) => e.article.value);
  
  // 预添加一个大纲项目
  const [outlines, setOutlines] = useState(article.outline.length > 0 ? article.outline : [""]);

  useEffect(() => {
    dispatch(info({ ...article, outline: outlines }));
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
    <div className="info">
      {/* <h2>Article Outline</h2> */}
      <div className="outlines-container" style={{ maxHeight: '500px', overflowY: 'auto' }}>
        <label>Outline</label>
        {outlines.map((outline, index) => (
          <div key={index} className="outline-item">
            <input
              type="text"
              value={outline}
              onChange={(e) => handleChange(index, e.target.value)}
              className="outline-input"
              placeholder="Enter outline detail here..."
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

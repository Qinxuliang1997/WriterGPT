import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";

const Outline = () => {
  const dispatch = useDispatch();
  const description = useSelector((e) => e.description.value);
  const [outlines, setOutlines] = useState(() => {
    if (description && description.outline) {
      return Object.entries(description.outline).map(([section, details]) => ({
        title: details.title,
        length: details.length,
        paragraphs: Object.entries(details.paragraphs).map(([_, p]) => p.content)
      }));
    }
    return [{ title: "", length: "", paragraphs: [""] }];
  });

  useEffect(() => {
    let outlineStructure = {};
    outlines.forEach((outline, index) => {
      outlineStructure[`小节 ${index + 1}`] = {
        title: outline.title,
        length: outline.length,
        paragraphs: outline.paragraphs.reduce((acc, content, idx) => {
          acc[`段落 ${idx + 1}`] = { content };
          return acc;
        }, {})
      };
    });
    dispatch(info({ ...description, outline: outlineStructure }));
  }, [outlines]);

  const handleChange = (sectionIndex, paragraphIndex, value) => {
    const newOutlines = [...outlines];
    newOutlines[sectionIndex].paragraphs[paragraphIndex] = value;
    setOutlines(newOutlines);
  };

  const addOutline = (index) => {
    const newOutlines = [...outlines];
    newOutlines.splice(index + 1, 0, { title: "", length: "", paragraphs: [""] });
    setOutlines(newOutlines);
  };

  const removeOutline = (index) => {
    const newOutlines = outlines.filter((_, idx) => idx !== index);
    setOutlines(newOutlines);
  };

  const addParagraph = (sectionIndex) => {
    const newOutlines = [...outlines];
    newOutlines[sectionIndex].paragraphs.push("");
    setOutlines(newOutlines);
  };

  const removeParagraph = (sectionIndex, paragraphIndex) => {
    const newOutlines = [...outlines];
    newOutlines[sectionIndex].paragraphs = newOutlines[sectionIndex].paragraphs.filter((_, idx) => idx !== paragraphIndex);
    setOutlines(newOutlines);
  };

  return (
    <div className="outline">
      <label>目录</label>
      <div className="outlines-container">
        {outlines.map((outline, sectionIndex) => (
          <div key={sectionIndex} className="outline-section">
            <div className="section-item">
                <input
                type="text"
                value={`${sectionIndex + 1} ${outline.title}`}
                onChange={(e) => {
                    const newOutlines = [...outlines];
                    const newTitle = e.target.value.replace(`${sectionIndex + 1} `, '');
                    newOutlines[sectionIndex].title = newTitle;
                    setOutlines(newOutlines);
                }}
                placeholder="编辑小节标题"
                />
                <button className="add-btn section-btn" onClick={() => addOutline(sectionIndex)}>➕</button>
                {outlines.length > 1 && (
                <button className="delete-btn section-btn" onClick={() => removeOutline(sectionIndex)}>✖️</button>
                )}
            </div>
            {outline.paragraphs.map((content, paragraphIndex) => (
              <div key={paragraphIndex} className="paragraph-container">
                <div className="paragraph-item">
                    <input
                    type="text"
                    value={`${sectionIndex + 1}.${paragraphIndex + 1} ${content}`}
                    onChange={(e) => {
                        const newOutlines = [...outlines];
                        const newContent = e.target.value.replace(`${sectionIndex + 1}.${paragraphIndex + 1} `, '');
                        newOutlines[sectionIndex].paragraphs[paragraphIndex] = newContent;
                        setOutlines(newOutlines);
                    }}
                    placeholder="编辑段落内容"
                    />
                    <button className="add-btn paragraph-btn" onClick={() => addParagraph(sectionIndex)}>➕</button>
                    <button className="delete-btn paragraph-btn" onClick={() => removeParagraph(sectionIndex, paragraphIndex)}>✖️</button>
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Outline;

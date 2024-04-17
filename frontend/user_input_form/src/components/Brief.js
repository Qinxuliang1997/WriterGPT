import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect,useRef} from "react";

const Brief = () => {
  const dispatch = useDispatch();
  const article = useSelector(e => e.article.value);
  const [perinfo, setPer] = useState({
    topic: "",
    primaryKeyword: "",
    secondaryKeywords: "",
    tone: "",
    view: "",
  });
  const refTopic=useRef();
  const refPrimaryKeywords=useRef();
  const refSecondaryKeywords=useRef();
  const refTone=useRef();
  const refView=useRef();

  useEffect(()=>{
    refTopic.current.value=article.topic;
    refPrimaryKeywords.current.value=article.primaryKeyword;
    refSecondaryKeywords.current.value=article.secondaryKeywords;
    refTone.current.value=article.tone;
    refView.current.value=article.view;
    dispatch(info({...article,topic:refTopic.current.value,primaryKeyword:refPrimaryKeywords.current.value,secondaryKeywords:refSecondaryKeywords.current.value,tone:refTone.current.value,view:refView.current.value}));
  },[])  

  useEffect(() => {
    dispatch(info({...article,topic:refTopic.current.value,primaryKeyword:refPrimaryKeywords.current.value,secondaryKeywords:refSecondaryKeywords.current.value,tone:refTone.current.value,view:refView.current.value}));
  }, [perinfo.topic, perinfo.primaryKeyword, perinfo.secondaryKeywords, perinfo.tone, perinfo.view]);

  return (
    <div className="info">
      {/* <h2>Article Description</h2> */}
      <form className="form" autoComplete="on">
        <div className="fields">
          <label>Topic</label>
          <input
            type="textarea" ref={refTopic} autoComplete="on"
            placeholder="e.g. Story about electric vehicle"
            onChange={e => setPer({ ...perinfo, topic: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>Primary Keyword</label>
          <input
            type="text" ref={refPrimaryKeywords} autoComplete="on"
            placeholder="e.g. Electric Vehicle"
            onChange={e => setPer({ ...perinfo, primaryKeyword: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>Secondary Keywords</label>
          <input
            type="text" ref={refSecondaryKeywords} autoComplete="on"
            placeholder="e.g. Supply Chain"
            onChange={e => setPer({ ...perinfo, secondaryKeywords: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>Tone</label>
          <select
            ref={refTone}
            onChange={e => setPer({ ...perinfo, tone: e.target.value})}
          >
            <option value="Casual">随意</option>
            <option value="Professional">专业</option>
            <option value="Formal">正式</option>
          </select>
        </div>
        <div className="fields">
          <label>View</label>
          <select
            ref={refView}
            onChange={e => setPer({ ...perinfo, view: e.target.value})}
          >
            <option value="First Person Singular">第一人称</option>
            <option value="Second Person Singular">第二人称</option>
            <option value="Third Person Singular">第三人称</option>
          </select>
        </div>

      </form>
    </div>
  );
};

export default Brief;

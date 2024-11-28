import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect, useRef } from "react";
import axios from 'axios'; // Import axios for API requests

const Brief = () => {
  const dispatch = useDispatch();
  const description = useSelector(e => e.description.value);
  const [perinfo, setPer] = useState({    
    occasion: "",
    topic: "",
    length: "",
    contentSuggestion: "",
    styleSuggestion: "",
  });
  const refOccasion = useRef();
  const refTopic = useRef();
  const refLength = useRef();
  const refContentSuggestion = useRef();
  const refStyleSuggestion = useRef();

  useEffect(()=>{
    refOccasion.current.value = description.occasion;
    refTopic.current.value = description.topic;
    refLength.current.value = description.length;
    refContentSuggestion.current.value = description.contentSuggestion;
    refStyleSuggestion.current.value = description.styleSuggestion;
  },[])  

  useEffect(() => {
    dispatch(info({...description, length: refLength.current.value, occasion: refOccasion.current.value, topic: refTopic.current.value, contentSuggestion: refContentSuggestion.current.value, styleSuggestion: refStyleSuggestion.current.value}));
  }, [perinfo.length, perinfo.occasion, perinfo.topic, perinfo.contentSuggestion, perinfo.styleSuggestion]);

  const fetchSuggestions = async () => {
    try {
      const response = await axios.post('http://106.14.184.241/api/topicsuggestion/', {'occasion': perinfo.occasion, 'topic': perinfo.topic}, {
        headers: {
          'Content-Type': 'application/json',
        }}
      );
      console.log('成功发送：', response.data);
      setPer({
        ...perinfo,
        contentSuggestion: response.data.content_suggestion,
        styleSuggestion: response.data.style_suggestion
      });
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  return (
    <div className="brief">
      <form className="form" autoComplete="on">
        <div className="fields">
          <label>使用场合</label>
          <input
            type="textarea" ref={refOccasion} autoComplete="on" required
            placeholder="例子： 市长在全市青年干部会议中的发言稿"
            onChange={e => setPer({ ...perinfo, occasion: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>主题（选填）</label>
          <input
            type="textarea" ref={refTopic} autoComplete="on"
            placeholder=""
            onChange={e => setPer({ ...perinfo, topic: e.target.value })}
          />
        </div>
        <div className="fields">
          <button type="button" onClick={fetchSuggestions}>获取内容和风格建议</button>
        </div>
        <div className="fields">
          <label>文章篇幅</label>
          <select
            ref={refLength}
            onChange={e => setPer({ ...perinfo, length: e.target.value })}
            required
          >
            <option value="500">500字</option>
            <option value="1000">1000字</option>
            <option value="2000">2000字</option>
            <option value="3000">3000字</option>
            <option value="4000">4000字</option>
            <option value="5000">5000字</option>
            <option value="大于5000">更多</option>
          </select>
        </div>
        <div className="fields-row">
          <div className="fields half">
            <label>详细内容</label>
            <textarea
              ref={refContentSuggestion} autoComplete="on" required
              value={perinfo.contentSuggestion}
              onChange={e => setPer({ ...perinfo, contentSuggestion: e.target.value })}
            />
          </div>
          <div className="fields half">
            <label>文章风格</label>
            <textarea
              ref={refStyleSuggestion} autoComplete="on" required
              value={perinfo.styleSuggestion}
              onChange={e => setPer({ ...perinfo, styleSuggestion: e.target.value })}
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default Brief;

import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect,useRef} from "react";

const Brief = () => {
  const dispatch = useDispatch();
  const description = useSelector(e => e.description.value);
  const [perinfo, setPer] = useState({
    title: "",
    topic: "",
    // primaryKeyword: "",
    // secondaryKeywords: "",
    // tone: "",
    style: "",
    length: "",
  });
  const refTitle=useRef();
  const refTopic=useRef();
  // const refPrimaryKeywords=useRef();
  // const refSecondaryKeywords=useRef();
  // const refTone=useRef();
  const refStyle=useRef();
  const refLength=useRef();

  useEffect(()=>{
    refTitle.current.value=description.title;
    refTopic.current.value=description.topic;
    // refPrimaryKeywords.current.value=description.primaryKeyword;
    // refSecondaryKeywords.current.value=description.secondaryKeywords;
    // refTone.current.value=description.tone;
    refStyle.current.value=description.style;
    refLength.current.value=description.length;
    dispatch(info({...description,title:refTitle.current.value,topic:refTopic.current.value,style:refStyle.current.value,length:refLength.current.value}));
  },[])  

  useEffect(() => {
    dispatch(info({...description,title:refTitle.current.value,topic:refTopic.current.value,style:refStyle.current.value,length:refLength.current.value}));
  }, [perinfo.title, perinfo.topic, perinfo.primaryKeyword, perinfo.secondaryKeywords, perinfo.style, perinfo.length]);

  return (
    <div className="brief">
      {/* <h2>Article Description</h2> */}
      <form className="form" autoComplete="on">
      <div className="fields">
          <label>标题</label>
          <input
            type="textarea" ref={refTitle} autoComplete="on"
            // placeholder="e.g. 新能源汽车的发展现状与未来展望"
            onChange={e => setPer({ ...perinfo, title: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>内容要求</label>
          <input
            type="textarea" ref={refTopic} autoComplete="on"
            // placeholder="e.g. 新能源汽车产业发展情况汇报"
            onChange={e => setPer({ ...perinfo, topic: e.target.value})}
          />
        </div>      
        {/* <div className="fields-row"> */}
            <div className="fields half">
              <label>稿件类型</label>
              <select
                ref={refStyle}
                onChange={e => setPer({ ...perinfo, style: e.target.value})}
              >
                <option value="专题研究报告">专题研究报告</option>
                <option value="个人工作总结">个人工作总结</option>
                <option value="讲话稿">讲话稿</option>
                <option value="新闻推送">新闻推送</option>
                <option value="行动计划">行动计划</option>
                {/* <option value="Third Person Singular">政策文件</option> */}
                {/* <option value="Third Person Singular"></option> */}
              </select>
            </div>
            <div className="fields half">
              <label>字数</label>
              <select
                ref={refLength}
                onChange={e => setPer({ ...perinfo, length: e.target.value})}
              >
                <option value="500">500字</option>
                <option value="1000">1000字</option>
                <option value="2000">2000字</option>
                <option value="3000">3000字</option>
                <option value="4000">4000字</option>
                <option value="5000">5000字</option>
              </select>
            </div>          
          {/* </div>   */}
      </form>
    </div>
  );
};

export default Brief;

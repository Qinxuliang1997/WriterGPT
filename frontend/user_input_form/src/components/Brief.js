import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect, useRef } from "react";
import { next } from '../features/pages'

const Brief = () => {
  const dispatch = useDispatch();
  const description = useSelector(e => e.description.value);
  const [perinfo, setPer] = useState({    
    occasion: "",
    content_requirement: "",
    length: "",
  });
  const refOccasion = useRef();
  const refContentRequirement = useRef();
  const refLength = useRef();

  useEffect(()=>{
    refOccasion.current.value = description.occasion;
    refContentRequirement.current.value = description.content_requirement;
    refLength.current.value = description.length;
  },[])  

  useEffect(() => {
    dispatch(info({...description, length: refLength.current.value, occasion: refOccasion.current.value, content_requirement: refContentRequirement.current.value}));
  }, [perinfo.length, perinfo.occasion, perinfo.content_requirement]);

  return (
    <div className="brief">
      <form className="form" autoComplete="on">
        <div className="fields">
          <label>使用场合</label>
          <input
            type="textarea" ref={refOccasion} autoComplete="on" required
            placeholder="市长在全市青年干部会议中的发言稿"
            onChange={e => setPer({ ...perinfo, occasion: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>内容要求（选填）</label>
          <textarea
            ref={refContentRequirement} autoComplete="on" required
            placeholder="文章包括三个部分，依次是......"
            onChange={e => setPer({ ...perinfo, content_requirement: e.target.value})}
          />
        </div>
        <div className="fields">
          <label>文章篇幅</label>
          <select
            ref={refLength}
            onChange={e => setPer({ ...perinfo, length: e.target.value })}
            required
            // value={perinfo.length || "1000"}
          >
            <option value="1000">1000字</option>
            <option value="2000">2000字</option>
            <option value="3000">3000字</option>
            <option value="4000">4000字</option>
            <option value="5000">5000字</option>
            <option value="大于5000">更多</option>
          </select>
        </div>
      </form>
      <div className={'btnNavigation btnRight'}>
        <button className='btn2' onClick={() => dispatch(next())}>{"下一步"}</button>
      </div>
    </div>
  );
};

export default Brief;

import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect,useRef} from "react";

const Title = () => {
  const dispatch = useDispatch();
  const article = useSelector(e => e.article.value);
  const [perinfo, setPer] = useState({
    title: "",
  });
  const refTitle=useRef();

  useEffect(()=>{
    refTitle.current.value=article.title;
    dispatch(info({...article,title:refTitle.current.value,}));
  },[])  

  useEffect(() => {
    dispatch(info({...article,title:refTitle.current.value,}));
  }, [perinfo.title]);


  return (
    <div className="info">
      <h2>Article Title</h2>
      <form className="form" autoComplete="on">
        <div className="fields">
          <label>Title</label>
          <input
            type="textarea" ref={refTitle} autoComplete="on"
            placeholder="e.g. Electric vehicle, one araising vast market!"
            onChange={e => setPer({ ...perinfo, title: e.target.value})}
          />
        </div>

      </form>
    </div>
  );
};

export default Title;

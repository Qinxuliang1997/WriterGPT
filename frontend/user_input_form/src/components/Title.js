import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect,useRef} from "react";

const Title = () => {
  const dispatch = useDispatch();
  const description = useSelector(e => e.description.value);
  const [perinfo, setPer] = useState({
    title: "",
  });
  const refTitle=useRef();

  useEffect(()=>{
    refTitle.current.value=description.title;
    dispatch(info({...description,title:refTitle.current.value,}));
  },[])  

  useEffect(() => {
    dispatch(info({...description,title:refTitle.current.value,}));
  }, [perinfo.title]);


  return (
    <div className="title">
      {/* <h2>Article Title</h2> */}
      <form className="form" autoComplete="on">
        <div className="fields">
          <label>标题</label>
          <input
            type="textarea" ref={refTitle} autoComplete="on"
            placeholder="e.g. 新能源汽车的发展现状与未来展望"
            onChange={e => setPer({ ...perinfo, title: e.target.value})}
          />
        </div>

      </form>
    </div>
  );
};

export default Title;

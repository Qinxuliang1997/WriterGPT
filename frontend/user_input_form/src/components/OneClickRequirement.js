import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { info } from "../features/description";
import { useState, useEffect,useRef} from "react";
import GenerateArticleOneClickButton from "./GenerateArticleOneClickButton";


const OneClickRequirement = () => {
  const dispatch = useDispatch();
  const description = useSelector(e => e.description.value);
  const [perinfo, setPer] = useState({
    content_requirement: "",
  });
  const refContentRequirement=useRef();

  useEffect(()=>{
    refContentRequirement.current.value=description.content_requirement;
    dispatch(info({...description,content_requirement:refContentRequirement.current.value}));
  },[])  

  useEffect(() => {
    dispatch(info({...description,content_requirement:refContentRequirement.current.value}));
  }, [perinfo.content_requirement]);

  return (
    <main>
      <div className="oneclickhead"></div>       
      <div className="Container"> 
        <div className="content">
          {/* <h2 className="oneclickheadtext">文章要求</h2> */}
          <div className="oneclickRequirement">
            <form className="form" autoComplete="on">
              <div className="fields">
                  {/* <label>文章要求</label> */}
                  <textarea
                    ref={refContentRequirement} autoComplete="on" required
                    onChange={e => setPer({ ...perinfo, content_requirement: e.target.value})}
                    placeholder="请在此输入你对文章的要求"
                  />
              </div>
            </form>   
            <GenerateArticleOneClickButton></GenerateArticleOneClickButton>  
          </div>
        </div>            
      </div>   
    </main>
  );
};

export default OneClickRequirement;

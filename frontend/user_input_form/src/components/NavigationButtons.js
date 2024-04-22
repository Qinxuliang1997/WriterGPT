import React from 'react'
import { useDispatch} from 'react-redux'
import { next } from '../features/pages'
import { useSelector } from 'react-redux'
import { back } from '../features/pages'
import { info } from '../features/description'

const NavigationButtons = () => {
  const page=useSelector((e)=>e.page.value);
  const article=useSelector(e=>e.article.value)
  const dispatch=useDispatch();
  const nextClick=()=>{
    console.log(article)
    dispatch(info({...article,nextClick:true}));
    if(page===0){
      dispatch(next());
      dispatch(info({...article,nextClick:false}))
    }
    if(page!==0){
      dispatch(next());
    }
  }
  return (
    <div className={page===0?'btnNavigation btnRight':'btnNavigation'}>
      {page!==0 &&<button className='btn1' onClick={()=>dispatch(back())}>上一步</button>}
      <button className='btn2'onClick={nextClick}>{"下一步"}</button>
    </div>
  )
}

export default NavigationButtons
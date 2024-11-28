import React from 'react'
import Step from "./Step"
import { useSelector } from 'react-redux'

const Steps = () => {
  const page=useSelector((e)=>e.page.value)
  return (
    <div className='Steps'>
      <Step step={1} title={"主题"} active={page===0}/>
      <Step step={2} title={"参考"} active={page===1}/>
      {/* <Step step={3} title={"标题"} active={page===2}/> */}
      <Step step={3} title={"提纲"} active={page>=2}/>
    </div>
  )
}

export default Steps
import Steps from "./components/Steps";
import Brief from "./components/Brief";
import NavigationButton from "./components/NavigationButtons"
import Reference from "./components/Reference"
import Title from "./components/Title"
import Outline from "./components/Outline"
import { useState } from "react";
import { useSelector } from "react-redux";
function App() {
  
  const page=useSelector((e)=>e.page.value)
  const PageDisplay=()=>{
    switch(page){
      case 0:
        return <Brief/>
      case 1:
        return <Reference/>
      case 2:
        return <Title/>
      case 3:
        return <Outline/> 
    //   case 4:
    //     return <Process/>
    }
  }
  return (
    <main>
      <div className="Container">
        {/* <Steps/> */}
        <div className="content">
        {PageDisplay()}
        {page !=4 && <NavigationButton/>} 
        </div>
      </div>
      
    </main>
  );
}

export default App;

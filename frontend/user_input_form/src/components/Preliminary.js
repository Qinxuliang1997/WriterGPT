import Steps from "./Steps";
import Brief from "./Brief";
import NavigationButton from "./NavigationButtons"
import Reference from "./Reference"
import Title from "./Title"
import Outline from "./Outline"
import { useSelector } from "react-redux";
import GenerateButton from "./GenerateButton";

function Preliminary() {
  
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
    }
  }
  return (
    <main>
      <Steps/>
      <div className="Container">
        <div className="content">
          {PageDisplay()}
          {page !=3 && <NavigationButton/>} 
          {page ==3 && <GenerateButton/>}
        </div>
      </div>
    </main>
  );
}

export default Preliminary;

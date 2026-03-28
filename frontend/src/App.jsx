import Dashboard from "./components/Dashboard";
import JDInput from "./components/JDInput";
import Upload from "./components/Upload";
import { getRankings } from "./api/api";
import { useEffect, useState } from "react";
function App() {


  const [data,setData] = useState([]);

    useEffect(() => {
      fetchData();
    }, []);

    const fetchData = async () => {
    const res = await getRankings();
    console.log(res)
    setData(res);
  };

  
  return (
    <div>
      <h1>Resume Screener</h1>
      <Upload onUploadSuccess = {fetchData} />
      <JDInput />
      <Dashboard data = {data} />
    </div>
  );
}

export default App;
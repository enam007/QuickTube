import "./App.css";
import Overview from "./Components/Overview";
import Search from "./Components/Search";
import Video from "./Components/Video";
import DataContext from "./Utills/DataContext";
import { useState } from "react";
import UrlContext from "./Utills/UrlContext";
import TimeContext from "./Utills/TimeContext";

function App() {
  const [masterData, setMasterData] = useState([]);
  const [url, setUrl] = useState("");
  const [time, setTime] = useState(0);
  return (
    <DataContext.Provider value={{ masterData, setMasterData }}>
      <UrlContext.Provider value={{ url, setUrl }}>
        <TimeContext.Provider value={{ time, setTime }}>
          <Search />
          <div className="container">
            <Video />
            <Overview />
          </div>
        </TimeContext.Provider>
      </UrlContext.Provider>
    </DataContext.Provider>
  );
}

export default App;

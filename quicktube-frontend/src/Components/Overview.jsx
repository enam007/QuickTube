import Summary from "./Summary";
import { DATA } from "../config";
import { useContext, useState, useEffect } from "react";
import DataContext from "../Utills/DataContext";
import { searchObjects } from "../Utills/helper";
import SearchHighlighter from "./Highlightedtext";
// const objectKeys = Object.keys(DATA);

// // Process each object using a loop or map
// const processedData = objectKeys.map((key) => {
//   const { start, overview, data } = DATA[key];
//   return { start, overview, data };
// });

//console.log("data", processedData);

const Overview = () => {
  const { masterData, setMasterData } = useContext(DataContext);
  const [searchText, setSearchText] = useState("");
  const [filterData, setFilterData] = useState(masterData);

  useEffect(() => {
    setFilterData(masterData);
  }, [searchText, masterData]);
  const handleSearch = () => {
    console.log(searchText);
    const result = searchObjects(masterData, searchText);
    console.log("result: ", result);
    setFilterData(result);
  };

  const handleSearchChange = (e) => {
    setSearchText(e.target.value);
  };

  console.log("masterData", masterData);
  console.log(filterData);
  return (
    <div className="txt-container">
      <div className="search">
        <input
          type="text"
          placeholder="Search in video"
          onChange={handleSearchChange}
          onKeyDown={(e) => {
            e.key === "Enter" && handleSearch();
          }}
          value={searchText}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      <div className="overview-card">
        {filterData.map((data, index) => {
          return (
            <>
              <Summary
                key={index}
                dataa={data}
                searchTerm={searchText}
              ></Summary>
            </>
          );
        })}
      </div>
    </div>
  );
};

export default Overview;

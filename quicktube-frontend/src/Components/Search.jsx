import { useState, useContext } from "react";
import DataContext from "../Utills/DataContext";
import UrlContext from "../Utills/UrlContext";

const Search = () => {
  const { masterData, setMasterData } = useContext(DataContext);
  const { url, setUrl } = useContext(UrlContext);
  const [searchText, setSearchText] = useState("");
  const handleSearch = (e) => {
    setSearchText(e.target.value);
  };

  async function handleApiCall() {
    try {
      setUrl(searchText);
      console.log(searchText);
      const response = await fetch(
        `http://127.0.0.1:5000/transcribe?url=${searchText}`
      );
      if (!response.ok) {
        throw new Error("Query Limit Exhausted");
      }
      const api_data = await response.json();
      console.log("api_data", api_data);
      const objectKeys = Object.keys(api_data);
      console.log(objectKeys);
      // Process each object using a loop or map
      const processedData = objectKeys.map((key) => {
        const { start, overview, data } = api_data[key];
        return { start, overview, data };
      });
      setMasterData(processedData);
      return processedData;
    } catch (e) {
      console.error("API REQUEST FAILED", e);
      throw e;
    }
  }

  return (
    <div className="search">
      <input
        type="text"
        placeholder="Enter URL"
        onChange={handleSearch}
        onKeyDown={(e) => {
          e.key === "Enter" && handleSearch();
        }}
        value={searchText}
      />
      <button onClick={handleApiCall}>Summarize</button>
    </div>
  );
};

export default Search;

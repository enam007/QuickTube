import { useContext, useEffect, useState } from "react";
import UrlContext from "../Utills/UrlContext";
const useVideo = () => {
  const { url, setUrl } = useContext(UrlContext);
  const [data, setData] = useState({});
  useEffect(() => {
    getData();
  }, [url]);

  async function getData() {
    const response = await fetch(`http://localhost:5000/video_info?url=${url}`);
    if (!response.ok) {
      throw new Error("Couldn't get video");
    }
    const video_info = await response.json();
    setData(video_info);
  }
  return [data, setData];
};

export default useVideo;

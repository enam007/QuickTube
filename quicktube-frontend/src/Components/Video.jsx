import { useContext, useEffect, useState } from "react";
import useVideo from "../Hooks/useVideo";
import TimeContext from "../Utills/TimeContext";
import VideoPlayer from "./YoutubeVideo";

const Video = () => {
  const [data, setData] = useVideo();
  const { time, setTime } = useContext(TimeContext);
  console.log("time", time);
  //let embed_code = data.embed_code + "&start=" + time;
  console.log("dataaa", data.url);
  return (
    <div className="video-card">
      <h4>Video</h4>
      <VideoPlayer time={time} url={data.url} type={data.video_type} />
      <h4>{data.title}</h4>
    </div>
  );
};

export default Video;

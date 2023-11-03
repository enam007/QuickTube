import { useState, useRef, useEffect } from "react";
import ReactPlayer from "react-player";

function VideoPlayer({ url, type, time }) {
  const [startTime, setStartTime] = useState(0); // Initial start time
  const playerRef = useRef(null);
  console.log(url, type, time);
  useEffect(() => {
    if (time !== undefined) {
      setStartTime(time);
      if (playerRef.current) {
        playerRef.current.seekTo(time);
      }
    }
  }, [time]);

  const onReady = () => {
    // Seek to the specified start time when the player is ready
    if (playerRef.current) {
      playerRef.current.seekTo(startTime, "seconds");
    }
  };

  const getConfig = () => {
    if (type === "youtube") {
      return {
        youtube: {
          playerVars: {
            start: startTime,
          },
        },
      };
    } else if (type === "vimeo") {
      return {
        vimeo: {
          playerOptions: {
            start: startTime,
          },
        },
      };
    } else {
      // Default config for other types (adjust as needed)
      return {};
    }
  };

  return (
    <div>
      <ReactPlayer
        url={url}
        ref={playerRef}
        controls={true}
        onStart={onReady}
        playing
        width="560px"
        height="315px"
        config={getConfig()}
      />
    </div>
  );
}

export default VideoPlayer;

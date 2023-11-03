import { DATA } from "../config";
import { useState, useContext } from "react";
import TimeContext from "../Utills/TimeContext";
import { getTime } from "../Utills/helper";
import useHighlightText from "../Hooks/useHighlighText";

const Snippets = ({ data, searchTerm }) => {
  console.log("data", data);
  const [isTranscript, setIsTranscript] = useState(false);
  const [buttonMessage, setIsButtonMessage] = useState("Transcript");
  const [headerMessage, setHeaderMessage] = useState("Summary");
  const highlightText = useHighlightText();
  const { time, setTime } = useContext(TimeContext);

  const handleTranscript = () => {
    setIsTranscript(!isTranscript);
    isTranscript
      ? (setIsButtonMessage("Transcript"), setHeaderMessage("Summary"))
      : (setIsButtonMessage("Summary"), setHeaderMessage("Transcript"));
  };
  const handleTime = (start) => {
    setTime(getTime(start));
  };
  return (
    <div className="snippets">
      <h3>{headerMessage}</h3>
      <div>
        {data.map((item, index) => {
          return (
            <div key={index}>
              <button onClick={() => handleTime(item.start)}>
                {item.start}
              </button>
              <button onClick={handleTranscript}>{buttonMessage}</button>
              {isTranscript ? (
                <p>{highlightText(item.text, searchTerm)}</p>
              ) : (
                <ul key={index}>
                  {item.summary.map((s, i) => {
                    return (
                      <>
                        {item.summary.length !== 1 && i === 0 ? (
                          <h3 key={i}>
                            {highlightText(
                              s.replace("Title:", "").trim(),
                              searchTerm
                            )}
                          </h3>
                        ) : (
                          <li key={i}>{highlightText(s.trim(), searchTerm)}</li>
                        )}
                      </>
                    );
                  })}
                </ul>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Snippets;

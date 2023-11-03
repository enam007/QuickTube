import Snippets from "./Snippets";
import { useState, useContext } from "react";
import TimeContext from "../Utills/TimeContext";
import { getTime } from "../Utills/helper";
import useHighlightText from "../Hooks/useHighlighText";

const Summary = ({ dataa, searchTerm }) => {
  const [isSeeMore, setIsSeeMore] = useState(false);
  const [buttonMessage, setButtonMessage] = useState("See Summary");
  const highlightText = useHighlightText();
  const { time, setTime } = useContext(TimeContext);
  const { start, overview, data } = dataa;

  console.log(dataa);

  const handleSeeMore = () => {
    setIsSeeMore(!isSeeMore);
    isSeeMore
      ? setButtonMessage("See Summary")
      : setButtonMessage("See Overview");
  };

  const handleTime = () => {
    setTime(getTime(start));
  };

  // const highlightedText = getHighlightedText(textToHighlight, searchTerm);

  console.log("data", time);
  return (
    <div className="summary-card">
      {!isSeeMore && (
        <ul>
          <h3>Overview</h3>
          <button onClick={handleTime}>{start}</button>
          {overview.map((d, index) => {
            return (
              <>
                {index === 0 ? (
                  <h3 key={index}>
                    {highlightText(d.replace("Title:", "").trim(), searchTerm)}
                  </h3>
                ) : (
                  <li key={index}>{highlightText(d.trim(), searchTerm)}</li>
                )}
              </>
            );
          })}
        </ul>
      )}
      <button className="btn-summary" onClick={handleSeeMore}>
        {buttonMessage}
      </button>
      {isSeeMore && <Snippets data={data} searchTerm={searchTerm} />}
    </div>
  );
};

export default Summary;

//import { useState } from "react";

// Custom hook for highlighting text
const useHighlightText = () => {
  const highlightText = (text, highlight) => {
    // Split on the highlight term and include it in parts, ignoring case
    const parts = text.split(new RegExp(`(${highlight})`, "gi"));

    return (
      <span>
        {" "}
        {parts.map((part, i) => (
          <span
            key={i}
            style={
              part.toLowerCase() === highlight.toLowerCase()
                ? { fontWeight: "bold", backgroundColor: "#ffd580" }
                : {}
            }
          >
            {part}
          </span>
        ))}{" "}
      </span>
    );
  };

  return highlightText;
};

export default useHighlightText;

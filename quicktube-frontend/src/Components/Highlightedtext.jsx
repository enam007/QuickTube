import { useEffect, useRef } from "react";
import Mark from "mark.js";

function SearchHighlighter({ content, searchTerms }) {
  console.log(content, searchTerms);
  const contentRef = useRef(null);

  useEffect(() => {
    const markInstance = new Mark(contentRef.current);

    // Highlight the search terms
    markInstance.mark(searchTerms, {
      className: "highlighted", // CSS class for highlighting
    });

    return () => {
      // Clean up when the component unmounts
      markInstance.unmark();
    };
  }, [content, searchTerms]);

  return <div ref={contentRef}>{content}</div>;
}

export default SearchHighlighter;

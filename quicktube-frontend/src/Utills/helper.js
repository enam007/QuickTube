export const getTime = (start) => {
  const [hours, minutes, seconds] = start.split(":").map(Number);
  const totalSeconds = hours * 3600 + minutes * 60 + seconds;
  return totalSeconds;
};

export const searchObjects = (objects, searchTerm) => {
  return objects.filter((object) => {
    // Search through 'overview' array
    if (Array.isArray(object.overview)) {
      const overviewMatch = object.overview.some((item) =>
        item.toLowerCase().includes(searchTerm.toLowerCase())
      );
      if (overviewMatch) return true;
    }

    // Search through 'data' array
    if (Array.isArray(object.data)) {
      const dataMatch = object.data.some((item) => {
        if (item.text.toLowerCase().includes(searchTerm.toLowerCase()))
          return true;

        // Search through 'summary' array in 'data' object
        if (Array.isArray(item.summary)) {
          return item.summary.some((summaryItem) =>
            summaryItem.toLowerCase().includes(searchTerm.toLowerCase())
          );
        }

        return false;
      });

      if (dataMatch) return true;
    }

    return false;
  });
};

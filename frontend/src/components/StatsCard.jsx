
function StatsCard({ title, data }) {
  const entries = Object.entries(data ?? {}).filter(([key, value]) => {
    if (key.startsWith("zone_") && key.endsWith("_percent")) {
      return true;
    }

    return true;
  }).filter(([key, value]) => {
    if (value === null || value === undefined || value === "") {
      return false;
    }

    const number = Number(value);
    return Number.isFinite(number);
  });

  return (
    <div className="stats-card">
      <h3>{title}</h3>
      {entries.map(([key, value]) => (
        <p key={key}>
          {key}: {Number(value).toFixed(3)}
        </p>
      ))}
    </div>
  );
}

export default StatsCard;

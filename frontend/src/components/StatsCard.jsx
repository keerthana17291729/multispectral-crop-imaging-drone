function StatsCard({ title, data }) {
    return (
        <div className="stats-card">
            <h3>{title}</h3>
            {Object.entries(data).map(([k, v]) => (
                <p key={k}>{k}: {Number(v).toFixed(3)}</p>
            ))}
        </div>
    )
}
export default StatsCard
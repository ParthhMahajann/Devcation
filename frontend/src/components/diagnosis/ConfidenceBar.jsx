export default function ConfidenceBar({ score, maxScore }) {
  const pct = maxScore > 0 ? Math.min((score / maxScore) * 100, 100) : 0
  return (
    <div className="w-full bg-slate-700 rounded-full h-2">
      <div
        className="h-2 rounded-full bg-gradient-to-r from-sky-500 to-violet-500 transition-all duration-500"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

const initialForm = {
  age: 29,
  vehicle_age_years: 4,
  prior_claims: 0,
  annual_mileage_thousands: 12,
}

export default function RiskPredictor() {
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: Number(value) }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (!res.ok) throw new Error('Prediction request failed')
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Risk Predictor</h2>
        <span className="tag">scikit-learn</span>
      </div>
      <p className="panel-desc">
        Logistic regression trained on synthetic policy data, served from the FastAPI backend.
      </p>

      <form onSubmit={handleSubmit} className="form-grid">
        <label>
          Age
          <input type="number" value={form.age} onChange={(e) => update('age', e.target.value)} />
        </label>
        <label>
          Vehicle age (years)
          <input type="number" value={form.vehicle_age_years} onChange={(e) => update('vehicle_age_years', e.target.value)} />
        </label>
        <label>
          Prior claims
          <input type="number" value={form.prior_claims} onChange={(e) => update('prior_claims', e.target.value)} />
        </label>
        <label>
          Annual mileage (000s)
          <input type="number" value={form.annual_mileage_thousands} onChange={(e) => update('annual_mileage_thousands', e.target.value)} />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Scoring…' : 'Predict risk'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className={`result result-${result.risk_label}`}>
          <span className="result-label">{result.risk_label.toUpperCase()} RISK</span>
          <span className="result-proba">{(result.risk_probability * 100).toFixed(1)}% confidence</span>
        </div>
      )}
    </section>
  )
}

import { useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

export default function PolicyBoard() {
  const [policies, setPolicies] = useState([])
  const [holderName, setHolderName] = useState('')
  const [vehicle, setVehicle] = useState('')
  const [error, setError] = useState(null)

  async function loadPolicies() {
    try {
      const res = await fetch(`${API_BASE}/policies`)
      setPolicies(await res.json())
    } catch {
      setError('Could not reach the backend')
    }
  }

  useEffect(() => {
    loadPolicies()
  }, [])

  async function addPolicy(e) {
    e.preventDefault()
    if (!holderName || !vehicle) return
    await fetch(`${API_BASE}/policies`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ holder_name: holderName, vehicle }),
    })
    setHolderName('')
    setVehicle('')
    loadPolicies()
  }

  async function removePolicy(id) {
    await fetch(`${API_BASE}/policies/${id}`, { method: 'DELETE' })
    loadPolicies()
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Policy Board</h2>
        <span className="tag">FastAPI</span>
      </div>
      <p className="panel-desc">In-memory CRUD to demonstrate the full request path end to end.</p>

      <form onSubmit={addPolicy} className="inline-form">
        <input placeholder="Holder name" value={holderName} onChange={(e) => setHolderName(e.target.value)} />
        <input placeholder="Vehicle" value={vehicle} onChange={(e) => setVehicle(e.target.value)} />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="policy-list">
        {policies.length === 0 && <li className="empty">No policies yet — add one above.</li>}
        {policies.map((p) => (
          <li key={p.id}>
            <span>{p.holder_name}</span>
            <span className="muted">{p.vehicle}</span>
            <button className="link" onClick={() => removePolicy(p.id)}>remove</button>
          </li>
        ))}
      </ul>
    </section>
  )
}

import { useState } from 'react'
import RiskPredictor from './components/RiskPredictor.jsx'
import PolicyBoard from './components/PolicyBoard.jsx'

const PIPELINE_STAGES = ['Checkout', 'Test', 'Train Model', 'Build Image', 'Deploy']

function App() {
  const [activeStage] = useState(PIPELINE_STAGES.length - 1)

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">ID</span>
          <div>
            <h1>IntelliDeploy</h1>
            <p className="subtitle">AI/ML-integrated CI/CD demo · Jenkins → Docker</p>
          </div>
        </div>
        <ol className="pipeline">
          {PIPELINE_STAGES.map((stage, i) => (
            <li key={stage} className={i <= activeStage ? 'done' : ''}>
              <span className="dot" />
              {stage}
            </li>
          ))}
        </ol>
      </header>

      <main className="grid">
        <RiskPredictor />
        <PolicyBoard />
      </main>

      <footer className="footer">
        Built by IntelliDeploy · FastAPI + scikit-learn + React, shipped via Jenkins
      </footer>
    </div>
  )
}

export default App

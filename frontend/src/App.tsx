import { HealthStatus } from './components/HealthStatus';

function App() {
  return (
    <div className="container">
      <header style={{ marginBottom: '2rem' }}>
        <h1>Orbit Hub</h1>
        <p style={{ color: '#6b7280' }}>AI/ML Developer Tools</p>
      </header>
      <main>
        <HealthStatus />
      </main>
    </div>
  );
}

export default App;
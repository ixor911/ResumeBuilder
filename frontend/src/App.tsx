import { backendEndpoints } from "./api/backendEndpoints";

function App() {
  const apiBaseUrl = backendEndpoints.meta.baseUrl;

  return (
    <main className="app-shell">
      <section className="workspace-panel">
        <p className="eyebrow">ResumeBuilder</p>
        <h1>Frontend workspace is ready</h1>
        <p>
          React, TypeScript, Vite, and the backend API layer are wired together.
        </p>
        <code>{apiBaseUrl}</code>
      </section>
    </main>
  );
}

export default App;

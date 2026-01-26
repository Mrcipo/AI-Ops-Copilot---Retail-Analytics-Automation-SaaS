import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState<"OK" | "ERROR" | "LOADING">("LOADING");

  useEffect(() => {
    fetch("/api/v1/health")
      .then((res) => (res.ok ? res.json() : Promise.reject()))
      .then(() => setStatus("OK"))
      .catch(() => setStatus("ERROR"));
  }, []);

  return (
    <div className="container">
      <h1>AI Ops Copilot</h1>
      <p className={status }>
        Backend status: {status}
      </p>
    </div>
  );
}

export default App;

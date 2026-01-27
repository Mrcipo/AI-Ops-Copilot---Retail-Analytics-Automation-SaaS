import { useEffect, useRef, useState } from "react";

function App() {
  const [status, setStatus] = useState<"OK" | "ERROR" | "LOADING">("LOADING");
  const didFetch = useRef(false);

  useEffect(() => {
    if (didFetch.current) {
      return;
    }
    didFetch.current = true;

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

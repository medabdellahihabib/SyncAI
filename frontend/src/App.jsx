import React, {useEffect, useState} from "react";
import axios from "axios";

export default function App(){
  const [sources, setSources] = useState([]);
  const [name, setName] = useState("");
  const [type, setType] = useState("postgres");

  useEffect(() => {
    fetchSources();
  }, []);

  async function fetchSources(){
    const res = await axios.get("http://localhost:8000/sources");
    setSources(res.data || []);
  }

  async function addSource(){
    await axios.post("http://localhost:8000/sources", {name, type, config: {}});
    setName("");
    fetchSources();
  }

  return (<div style={{padding:20}}>
    <h2>SyncAI - Dashboard</h2>
    <div>
      <input placeholder="name" value={name} onChange={e=>setName(e.target.value)} />
      <select value={type} onChange={e=>setType(e.target.value)}>
        <option value="postgres">Postgres</option>
        <option value="mongo">MongoDB</option>
      </select>
      <button onClick={addSource}>Add source</button>
    </div>

    <h3>Sources</h3>
    <ul>
      {sources.map(s => <li key={s.id}>{s.name} — {s.type}</li>)}
    </ul>
  </div>);
}

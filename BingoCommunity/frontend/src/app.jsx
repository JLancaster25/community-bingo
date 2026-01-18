import { Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { supabase } from "./supabase";
import BingoBoard from "./BingoBoard";
import AdminDashboard from "./AdminDashboard";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function signIn() {
    await supabase.auth.signInWithPassword({ email, password });
  }

  return (
    <div className="auth">
      <h2>Lan Games Bingo</h2>
      <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
      <input
        type="password"
        placeholder="Password"
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={signIn}>Login</button>
    </div>
  );
}

function AdminRoute({ user, children }) {
  const role = localStorage.getItem("role");
  if (!user || role !== "admin") return <Navigate to="/" />;
  return children;
}

export default function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      setUser(data?.user ?? null);
    });

    supabase.auth.onAuthStateChange((_e, session) => {
      setUser(session?.user ?? null);
    });
  }, []);

  return (
    <Routes>
      <Route path="/" element={user ? <BingoBoard user={user} /> : <Login />} />
      <Route
        path="/admin"
        element={
          <AdminRoute user={user}>
            <AdminDashboard />
          </AdminRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" />}/>
	  <Route path="/admin" element={<AdminDashboard />} />
    </Routes>
  );
}

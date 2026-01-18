import { useEffect, useState } from "react";
import { supabase } from "./supabase";

export default function AdminDashboard() {
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);

  async function loadRooms() {
    setLoading(true);

    const session = (await supabase.auth.getSession()).data.session;

    const res = await fetch(
      import.meta.env.VITE_API_URL + "/admin/rooms",
      {
        headers: {
          Authorization: `Bearer ${session.access_token}`
        }
      }
    );

    const data = await res.json();
    setRooms(data);
    setLoading(false);
  }

  async function kick(room, socketId) {
    const session = (await supabase.auth.getSession()).data.session;

    await fetch(
      import.meta.env.VITE_API_URL + "/admin/kick",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ room, socketId })
      }
    );

    loadRooms();
  }

  useEffect(() => {
    loadRooms();
  }, []);

  if (loading) {
    return <div className="panel">Loading admin dashboard…</div>;
  }

  return (
    <div className="admin">
      <h1>🛠 Admin Dashboard</h1>

      {rooms.length === 0 && <p>No active rooms</p>}

      {rooms.map(room => (
        <div key={room.code} className="admin-room">
          <h3>
            Room {room.code} ({room.players.length} players)
          </h3>

          {room.players.map(p => (
            <div key={p.socketId} className="admin-player">
              <span>{p.username ?? p.socketId}</span>
              <button
                className="danger"
                onClick={() => kick(room.code, p.socketId)}
              >
                Kick
              </button>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
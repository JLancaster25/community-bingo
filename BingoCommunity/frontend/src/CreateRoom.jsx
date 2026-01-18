import { useState } from "react";
import { io } from "socket.io-client";

const socket = io(import.meta.env.VITE_API_URL);

export default function CreateRoom() {
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");

  function createRoom() {
    socket.emit("create_room", { code, password });
    alert(`Invite link: ${window.location.origin}/?room=${code}`);
  }

  return (
    <div className="create-room">
      <input placeholder="Room Code" onChange={e => setCode(e.target.value.toUpperCase())} />
      <input
        type="password"
        placeholder="Room Password (optional)"
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={createRoom}>Create Private Room</button>
    </div>
  );
}

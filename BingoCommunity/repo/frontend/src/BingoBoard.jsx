import { useEffect, useState } from "react";
import { io } from "socket.io-client";

const socket = io(import.meta.env.VITE_API_URL, {
  autoConnect: true,
  reconnection: true
});

export default function BingoBoard({ user }) {
  const [room, setRoom] = useState("");
  const [card, setCard] = useState(null);
  const [call, setCall] = useState("");

  function joinRoom() {
    socket.emit("join_room", { code: room });
    localStorage.setItem("room", room);
  }

  useEffect(() => {
    socket.on("card", setCard);
    socket.on("number", data => {
      setCall(data.call);
      speechSynthesis.speak(new SpeechSynthesisUtterance(data.call));
    });

    // Auto-rejoin
    const savedRoom = localStorage.getItem("room");
    if (savedRoom) socket.emit("rejoin", { room: savedRoom });

    return () => {
      socket.off("card");
      socket.off("number");
    };
  }, []);

  return (
    <div className="bingo">
      <h2>{user.email}</h2>

      {!card && (
        <div className="room">
          <input
            placeholder="Room Code"
            onChange={e => setRoom(e.target.value.toUpperCase())}
          />
          <button onClick={joinRoom}>Join Room</button>
        </div>
      )}

      {call && <div className="call">🎤 {call}</div>}

      {card && (
        <div className="card">
          {Object.entries(card).map(([letter, nums]) => (
            <div key={letter} className="column">
              <strong>{letter}</strong>
              {nums.map((n, i) => (
                <div key={i} className={n === "X" ? "marked" : ""}>
                  {n}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

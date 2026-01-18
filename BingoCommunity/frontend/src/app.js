import { useEffect, useState } from "react";
speechSynthesis.speak(new SpeechSynthesisUtterance(data.call));
});


return () => socket.disconnect();
}, []);


const signIn = async (email, password) => {
const { data } = await supabase.auth.signInWithPassword({ email, password });
setUser(data.user);
};


const createRoom = () => socket.emit("create_room", { code: room });
const joinRoom = () => socket.emit("join_room", { code: room });
const draw = () => socket.emit("draw_number", { code: room });


const loadLeaderboard = async () => {
const { data } = await supabase.from("stats").select("username,wins").order("wins", { ascending: false });
setLeaderboard(data);
};


if (!user) {
return (
<div className="panel">
<h2>Login</h2>
<button onClick={() => signIn("test@example.com", "password")}>Quick Login</button>
</div>
);
}


return (
<div className="app">
<h1>🎱 Bingo</h1>


<input placeholder="Room Code" onChange={e => setRoom(e.target.value)} />
<button onClick={createRoom}>Create Room</button>
<button onClick={joinRoom}>Join Room</button>


{card && (
<div className="card">
{Object.values(card).flat().map((v,i)=>(
<div key={i} className={`cell ${v==='X'?'marked':''}`}>{v}</div>
))}
</div>
)}


<div className="callout">{callout}</div>
<button onClick={draw}>Draw</button>


<button onClick={loadLeaderboard}>Leaderboard</button>
{leaderboard.map((p,i)=>(
<div key={i}>{p.username}: {p.wins}</div>
))}
</div>
);
}
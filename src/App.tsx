import { useEffect, useState } from "react";
import { BuyTickets } from "./pages/BuyTickets";
import { Login } from "./pages/Login";
import { Toaster } from "./components/ui/toaster";

function App() {
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    setUsername(localStorage.getItem("username") || null);
  }, []);

  function handleLogout() {
    localStorage.removeItem("username");
    setUsername(null);
  }

  function handleLogin(username: string) {
    if (username) {
      localStorage.setItem("username", username);
      setUsername(username);
    }
  }

  return (
    <>
      {username ? (
        <BuyTickets username={username} handleLogout={handleLogout} />
      ) : (
        <Login handleLogin={handleLogin} />
      )}
      <Toaster />
    </>
  );
}

export default App;

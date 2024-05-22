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
      <div className="fixed top-0 left-0 right-0 bottom-0 w-full h-[100lvh] pointer-events-none bg-no-repeat bg-center bg-[url('./main_bg.webp')] -z-10">
        <div className="fixed top-0 left-0 right-0 bottom-0 w-full h-[100lvh]">
          <video autoPlay muted loop className="w-full h-full object-cover">
            <source src="./bg_mov.webm" type="video/webm" />
          </video>
        </div>
        <div className="fixed bottom-0 left-0 w-full min-w-[600px] h-[100lvh] bg-no-repeat bg-[center_bottom] bg-[url('./bg_island.webp')] bg-contain" />
      </div>
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

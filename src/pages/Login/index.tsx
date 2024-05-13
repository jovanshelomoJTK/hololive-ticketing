import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";

export const Login = ({
  handleLogin,
}: {
  handleLogin: (username: string) => void;
}) => {
  const [username, setUsername] = useState<string>("");
  return (
    <>
      Login
      <Input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <Button onClick={() => handleLogin(username)}>Login</Button>
    </>
  );
};

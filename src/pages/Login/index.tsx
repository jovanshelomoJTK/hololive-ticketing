import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useState } from "react";

export const Login = ({
  handleLogin,
}: {
  handleLogin: (username: string) => void;
}) => {
  const [username, setUsername] = useState<string>("");
  return (
    <div className="w-full h-full flex justify-center items-center p-4">
      <Card className="overflow-clip border-primary border-2 w-full max-w-[600px]">
        <CardHeader className="bg-primary text-primary-foreground">
          <CardTitle className="text-3xl font-extrabold">
            Login to Your Account
          </CardTitle>
        </CardHeader>
        <CardContent className="p-8">
          <Input
            className="mb-8 rounded-full p-4 w-full"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <Button
            onClick={() => handleLogin(username)}
            className="w-full tracking-wider"
            disabled={!username}
          >
            Login
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

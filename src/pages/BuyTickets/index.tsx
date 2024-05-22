import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { BuyDialog } from "./buyDialog";
import { useToast } from "@/components/ui/use-toast";

export type Stage = {
  stage_id: number;
  stage_name: string;
  stage_day: number;
  date_open: string;
  date_start: string;
  ticket_price: number;
  ticket_stock: number;
};

export type Ticket = {
  ticket_id: number;
  stage_id: number;
  timestamp: string;
  username: string;
};

export const BuyTickets = ({
  username,
  handleLogout,
}: {
  username: string;
  handleLogout: () => void;
}) => {
  const [stages, setStages] = useState<Stage[]>([]);
  const [myTickets, setMyTickets] = useState<Ticket[]>([]);
  const { toast } = useToast();

  const refreshData = useCallback(() => {
    fetch("http://localhost:4444/stages")
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          toast({
            title: "Error",
            description: data.error,
            variant: "destructive",
          });
          return;
        }

        setStages(data);
      })
      .catch((error) => {
        toast({
          title: "Failed to get stage data!",
          description: error.message,
          variant: "destructive",
        });
      });

    fetch("http://localhost:4444/my-tickets?username=" + username)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          toast({
            title: "Error",
            description: data.error,
            variant: "destructive",
          });
          return;
        }

        setMyTickets(data);
      })
      .catch((error) => {
        toast({
          title: "Failed to get ticket data!",
          description: error.message,
          variant: "destructive",
        });
      });
  }, [toast, username]);

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  return (
    <div className="w-full flex flex-col p-4 gap-4 max-w-[1700px] mx-auto">
      <Card className="overflow-clip border-secondary border-2 w-full">
        <CardHeader className="bg-secondary text-secondary-foreground">
          <CardTitle className="text-4xl font-extrabold">
            Your Account
          </CardTitle>
        </CardHeader>
        <CardContent className="p-8 space-y-4">
          <p>
            You are logged in as <strong>{username}</strong>
          </p>
          <Button onClick={handleLogout} variant="secondary">
            Logout
          </Button>
        </CardContent>
      </Card>
      <Card className="overflow-clip border-primary border-2 w-full">
        <CardHeader className="bg-primary text-primary-foreground">
          <CardTitle className="text-4xl font-extrabold">
            hololive 5th fes. Capture the Moment Supported By Bushiroad
          </CardTitle>
        </CardHeader>
        <CardContent className="p-8 space-y-4">
          {stages.map((stage) => (
            <Card key={stage.stage_id}>
              <CardHeader>
                <CardTitle>{stage.stage_name}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Day: {stage.stage_day}
                  <br />
                  Open: {new Date(stage.date_open).toLocaleString()}
                  <br />
                  Start: {new Date(stage.date_start).toLocaleString()}
                  <br />
                  Price: ¥{stage.ticket_price}
                  <br />
                  Stock: {stage.ticket_stock}
                </CardDescription>
              </CardContent>
              <CardFooter>
                <BuyDialog
                  stage={stage}
                  username={username}
                  refreshData={refreshData}
                />
              </CardFooter>
            </Card>
          ))}
        </CardContent>
      </Card>
      <Card className="overflow-clip border-secondary border-2 w-full">
        <CardHeader className="bg-secondary text-secondary-foreground">
          <CardTitle className="text-4xl font-extrabold">
            Bought Tickets
          </CardTitle>
        </CardHeader>
        <CardContent className="p-8 space-y-4">
          {!myTickets.length ? (
            <p>No tickets bought yet</p>
          ) : (
            myTickets.map((ticket) => (
              <Card key={ticket.ticket_id}>
                <CardHeader>
                  <CardTitle>
                    {
                      stages.find((stage) => stage.stage_id === ticket.stage_id)
                        ?.stage_name
                    }
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>
                    <p>{ticket.ticket_id}</p>
                    <p>{new Date(ticket.timestamp).toLocaleString()}</p>
                  </CardDescription>
                </CardContent>
              </Card>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};

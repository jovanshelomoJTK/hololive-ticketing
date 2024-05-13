import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Stage } from ".";
import { useState } from "react";
import { DialogClose } from "@radix-ui/react-dialog";
import { useToast } from "@/components/ui/use-toast";

export const BuyDialog = ({
  stage,
  username,
  refreshData,
}: {
  stage: Stage;
  username: string;
  refreshData: () => void;
}) => {
  const [ticketQuantity, setTicketQuantity] = useState<string>("1");
  const { toast } = useToast();

  function buyTickets() {
    fetch("http://localhost:4444/buy-tickets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        stage_id: stage.stage_id,
        username: username,
        qty: +ticketQuantity,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        // refresh the data
        refreshData();

        if (data.error) {
          toast({
            title: "Error",
            description: data.error,
            variant: "destructive",
          });
          return;
        }

        toast({
          title: "Tiket berhasil dibeli",
          description: `Berhasil membeli ${ticketQuantity} tiket untuk ${stage.stage_name}`,
          variant: "default",
        });
      })
      .catch((error) => {
        toast({
          title: "Gagal membeli tiket",
          description: error.message,
          variant: "destructive",
        });
      });
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button disabled={stage.ticket_stock === 0}>Beli</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Beli Tiket {stage.stage_name}</DialogTitle>
          <DialogDescription>description</DialogDescription>
        </DialogHeader>
        <p>min: 1, max: {stage.ticket_stock}</p>
        <Input
          placeholder="Jumlah Tiket"
          type="number"
          min={1}
          max={stage.ticket_stock}
          value={ticketQuantity}
          onChange={(e) => {
            setTicketQuantity(e.target.value);
          }}
          onBlur={(e) => {
            // check if the value is less than 1 or more than the stock
            if (parseInt(e.target.value) < 1) {
              setTicketQuantity("1");
            } else if (parseInt(e.target.value) > stage.ticket_stock) {
              setTicketQuantity(stage.ticket_stock.toString());
            }
          }}
        />
        <p>total: ¥{parseInt(ticketQuantity) * stage.ticket_price}</p>
        <DialogClose asChild>
          <Button onClick={buyTickets}>Beli</Button>
        </DialogClose>
      </DialogContent>
    </Dialog>
  );
};

import React, { useState, useContext } from "react";
import Modal from "./Modal";
import { AuthContext } from "../context/AuthContext";

export default function TicketPurchase({ event }) {
  const { user, token } = useContext(AuthContext);
  const [open, setOpen] = useState(false);
  const [ticketType, setTicketType] = useState("Regular");

  const handlePurchase = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/tickets", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          event_id: event.id,
          ticket_type: ticketType,
        }),
      });

      if (!res.ok) throw new Error("Purchase failed");
      const data = await res.json();
      alert("Ticket purchased successfully!");
      setOpen(false);
    } catch (err) {
      alert(err.message);
    }
  };

  if (!user) return <p className="text-red-500">Login to buy tickets</p>;

  return (
    <div>
      <button
        onClick={() => setOpen(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
      >
        Buy Ticket
      </button>

      <Modal isOpen={open} onClose={() => setOpen(false)}>
        <h2 className="text-lg font-bold mb-2">Buy Ticket for {event.title}</h2>
        <label className="block mb-2">
          Ticket Type:
          <select
            value={ticketType}
            onChange={(e) => setTicketType(e.target.value)}
            className="ml-2 border rounded p-1"
          >
            <option value="Regular">Regular</option>
            <option value="VIP">VIP</option>
          </select>
        </label>
        <button
          onClick={handlePurchase}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Confirm Purchase
        </button>
      </Modal>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import TicketPurchase from "../components/TicketPurchase";

export default function EventDetailPage() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/events/${id}`)
      .then((res) => res.json())
      .then(setEvent);
  }, [id]);

  if (!event) return <p>Loading...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">{event.title}</h1>
      <p>{event.description}</p>
      <p>Date: {new Date(event.date).toLocaleString()}</p>
      <p>Location: {event.location}</p>
      <p>Price: ${event.price}</p>

      <TicketPurchase event={event} />
    </div>
  );
}

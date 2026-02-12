import React from "react";

export default function ContactItem({ contact, deleteContact }) {
  return (
    <div className="contact-item">
      <div>
        <p><strong>{contact.name}</strong></p>
        <p>{contact.email}</p>
        {contact.phone && <p>{contact.phone}</p>}
      </div>
      <button onClick={() => deleteContact(contact.id)}>Delete</button>
    </div>
  );
}

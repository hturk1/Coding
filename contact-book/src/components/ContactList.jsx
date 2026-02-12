import React from "react";
import ContactItem from "./ContactItem";

export default function ContactList({ contacts, deleteContact, filterText }) {
  if (contacts.length === 0) {
    return (
      <p>{filterText ? `No matches found for '${filterText}'` : "No contacts yet. Add one above!"}</p>
    );
  }

  return (
    <div className="contact-list">
      {contacts.map(contact => (
        <ContactItem key={contact.id} contact={contact} deleteContact={deleteContact} />
      ))}
    </div>
  );
}

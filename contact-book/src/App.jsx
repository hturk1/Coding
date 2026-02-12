import React, { useState } from "react";
import ContactForm from "./components/ContactForm";
import SearchBar from "./components/SearchBar";
import ContactList from "./components/ContactList";

export default function App() {
  const [contacts, setContacts] = useState([]);
  const [filterText, setFilterText] = useState("");

  // add a new contact
  const addContact = (contact) => {
    setContacts([...contacts, { ...contact, id: Date.now().toString() }]);
  };

  // delete a contact by id
  const deleteContact = (id) => {
    setContacts(contacts.filter(contact => contact.id !== id));
  };

  // filter contacts by name or email
  const filteredContacts = contacts.filter(
    c =>
      c.name.toLowerCase().includes(filterText.toLowerCase()) ||
      c.email.toLowerCase().includes(filterText.toLowerCase())
  );

  return (
    <div className="container">
      <h1>Simple Contact Book</h1>
      <ContactForm addContact={addContact} />
      <SearchBar filterText={filterText} setFilterText={setFilterText} />
      <ContactList contacts={filteredContacts} deleteContact={deleteContact} filterText={filterText} />
    </div>
  );
}


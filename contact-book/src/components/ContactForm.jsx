import React, { useState } from "react";

export default function ContactForm({ addContact }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");

  // validate the inputs
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) {
      setError("Error: name and email are both required");
      return;
    }
    if (!email.includes("@")) {
      setError("Please enter a valid email.");
      return;
    }

    // add new contact
    addContact({ name, email, phone });
    setName("");
    setEmail("");
    setPhone("");
    setError("");
  };

  return (
    <form onSubmit={handleSubmit} className="contact-form">
      {error && <p className="error">{error}</p>}

      <label>Name</label>
      <input type="text" placeholder="e.g., John Doe" value={name} onChange={(e) => setName(e.target.value)} />

      <label>Email</label>
      <input type="email" placeholder="e.g., john@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />

      <label>Phone Number (optional)</label>
      <input type="tel" placeholder="e.g., 123-456-7890" value={phone} onChange={(e) => setPhone(e.target.value)} />

      <button type="submit">Add Contact</button>
    </form>
  );
}

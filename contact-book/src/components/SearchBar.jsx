import React from "react";

export default function SearchBar({ filterText, setFilterText }) {
  return (
    <input
      className="search-bar"
      type="text"
      placeholder="Search by name or email..."
      value={filterText}
      onChange={e => setFilterText(e.target.value)}
    />
  );
}

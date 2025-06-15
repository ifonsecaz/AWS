import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4 mb-4">
      <div className="flex space-x-4">
        <Link to="/" className="hover:underline">All Notes</Link>
        <Link to="/create" className="hover:underline">Create Note</Link>
      </div>
    </nav>
  );
};

export default Navbar;
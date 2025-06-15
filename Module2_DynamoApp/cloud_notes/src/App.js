import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateNote from './components/CreateNote';
import NoteList from './components/NoteList';
import ViewNote from './components/ViewNote';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="container mx-auto">
        <Routes>
          <Route path="/" element={<NoteList />} />
          <Route path="/create" element={<CreateNote onNoteCreated={() => window.location.href = '/'} />} />
          <Route path="/note/:noteId" element={<ViewNote />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
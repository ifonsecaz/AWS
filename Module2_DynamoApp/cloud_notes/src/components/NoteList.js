import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const NoteList = () => {
  const [notes, setNotes] = useState([]);

  const fetchNotes = async () => {
    const res = await axios.get('https://nbjyar8551.execute-api.us-east-1.amazonaws.com/get_all_notes');
    setNotes(res.data);
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">All Notes</h2>
      <ul className="space-y-2">
        {notes.map(note => (
          <li key={note.NoteID} className="border p-3 rounded shadow-md">
            <Link to={`/note/${note.NoteID}`} className="text-blue-500 font-semibold">
              {note.Title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NoteList;
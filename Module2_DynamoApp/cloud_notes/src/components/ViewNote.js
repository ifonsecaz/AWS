import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const ViewNote = () => {
  const { noteId } = useParams();
  const [note, setNote] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNote = async () => {
      const res = await axios.get(`https://ykbtknda16.execute-api.us-east-1.amazonaws.com/get_note/${noteId}`);
      setNote(res.data);
    };
    fetchNote();
  }, [noteId]);

  const handleDelete = async () => {
    await axios.delete(`https://6sty7z9bsb.execute-api.us-east-1.amazonaws.com/delete_note/${noteId}`);
    navigate('/');
  };
  

  if (!note) return <div>Loading...</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-2">{note.Title}</h2>
      <p className="mb-2">{note.Content}</p>
      <p className="text-sm text-gray-500 mb-4">Created At: {note.CreatedAt}</p>
      {note.FileURL && (
        <div className="mb-4">
          <a href={note.FileURL} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
            View Attached File
          </a>
        </div>
      )}
      <button onClick={handleDelete} className="bg-red-500 text-white px-4 py-2 rounded">
        Delete Note
      </button>
    </div>
  );
};

export default ViewNote;

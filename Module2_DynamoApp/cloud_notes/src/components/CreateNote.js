import React, { useState } from 'react';
import axios from 'axios';

const CreateNote = ({ onNoteCreated }) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      title,
      content,
    };

    if (file) {
      const reader = new FileReader();
      reader.onloadend = async () => {
        payload.fileName = file.name;
        payload.fileContent = reader.result.split(',')[1];

        const res = await axios.post('https://4fgna1jvze.execute-api.us-east-1.amazonaws.com/create_note', payload);
        onNoteCreated(res.data);
      };
      reader.readAsDataURL(file);
    } else {
      const res = await axios.post('https://4fgna1jvze.execute-api.us-east-1.amazonaws.com/create_note', payload);
      onNoteCreated(res.data);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 shadow-md rounded bg-white">
      <h2 className="text-xl font-bold mb-2">Create Note</h2>
      <input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} className="block w-full mb-2 p-2 border rounded" required />
      <textarea placeholder="Content" value={content} onChange={e => setContent(e.target.value)} className="block w-full mb-2 p-2 border rounded" required />
      <input type="file" onChange={e => setFile(e.target.files[0])} className="block mb-2" />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Create</button>
    </form>
  );
};

export default CreateNote;

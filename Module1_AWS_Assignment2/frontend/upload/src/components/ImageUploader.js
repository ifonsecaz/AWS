import React, { useState } from 'react';

const ImageUploader = () => {
  const [uploading, setUploading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const uploadImage = async (file) => {
    try {
      setUploading(true);
      setSuccessMessage('');
      setErrorMessage('');

      const res = await fetch('https://lud6eskzlh.execute-api.us-east-1.amazonaws.com/dev/', {
        method: 'POST',
        body: JSON.stringify({ filename: file.name }),
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await res.json();
      console.log(data);
      const upload = await fetch(data.uploadURL, {
        method: 'PUT',
        headers: { 'Content-Type': file.type },
        body: file
      });

      if (upload.ok) {
        setSuccessMessage('Upload successful!');
      } else {
        throw new Error('Upload failed');
      }

    } catch (err) {
      console.error(err);
      setErrorMessage('Something went wrong. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      uploadImage(file);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto', textAlign: 'center' }}>
      <h2>Upload Image to S3</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} disabled={uploading} />
      {uploading && <p>Uploading...</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default ImageUploader;
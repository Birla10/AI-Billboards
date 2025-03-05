import React from 'react';
import NavBar from './components/NavBar';
import UploadForm from './components/UploadForm';

function App() {
  return (
    <div>
      <NavBar />
      <main style={{ padding: "20px" }}>
        <UploadForm />
      </main>
    </div>
  );
}

export default App;
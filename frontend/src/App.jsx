import React, { useState } from "react";
import UploadPDF from "./UploadPDF";
import AskQuestion from "./AskQuestion";

function App() {
  const [filename, setFilename] = useState("");

  return (
    <div>
      <h1>PDF Q&A App</h1>
      <UploadPDF setFilename={setFilename} />
      {filename && <AskQuestion filename={filename} />}
    </div>
  );
}

export default App;

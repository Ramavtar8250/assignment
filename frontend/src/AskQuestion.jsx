import React, { useState } from "react";
import axios from "axios";

const AskQuestion = ({ filename }) => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    try {
      const response = await axios.post("http://localhost:8000/ask_question/", 
        new URLSearchParams({ filename, question })
      );
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error getting answer:", error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleAsk}>Ask</button>
      {answer && <p>Answer: {answer}</p>}
    </div>
  );
};

export default AskQuestion;

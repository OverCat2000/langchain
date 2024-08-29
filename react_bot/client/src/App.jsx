import React from "react";
import Chatbot from "./ChatBot"; // Make sure this path matches where your Chatbot component is located
import ChatApp from "./ChatApp";

const App = () => {
  return (
    <div>
      <h1>Chatbot Application</h1>
      <ChatApp />
    </div>
  );
};

export default App;

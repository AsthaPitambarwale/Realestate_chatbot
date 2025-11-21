import React, { useState } from "react";
import { MessageCircle, X } from "lucide-react";
import api from "../api"; // make sure this points to your axios instance

export default function AIHelpButton() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    setMessages([...messages, { sender: "user", text: input }]);
    const query = input;
    setInput("");
    setLoading(true);

    try {
      const res = await api.post("/query/", { query }); // call backend API
      const aiText = res.data.summary || "Sorry, I couldn't understand.";

      // Add AI response
      setMessages((prev) => [...prev, { sender: "ai", text: aiText }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "ai", text: "Error fetching response from AI." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 bg-indigo-600 hover:bg-indigo-700 
                   text-white p-4 rounded-full shadow-lg transition-all z-50"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Chat Popup */}
      {open && (
        <div className="fixed bottom-20 right-6 w-80 bg-white dark:bg-gray-800 shadow-xl rounded-xl flex flex-col overflow-hidden z-50">
          {/* Header */}
          <div className="flex justify-between items-center bg-indigo-600 text-white p-3">
            <span>AI Assistant</span>
            <button onClick={() => setOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-3 overflow-y-auto h-64 space-y-2">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-2 rounded-md max-w-[80%] break-words ${
                  msg.sender === "user"
                    ? "bg-indigo-100 text-indigo-900 self-end"
                    : "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 self-start"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="flex border-t border-gray-300 dark:border-gray-600">
            <input
              type="text"
              className="flex-1 p-2 outline-none bg-transparent text-gray-900 dark:text-gray-100"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={loading ? "AI is typing..." : "Ask something..."}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              disabled={loading}
            />
            <button
              onClick={handleSend}
              className={`bg-indigo-600 hover:bg-indigo-700 text-white px-4 ${
                loading ? "opacity-50 cursor-not-allowed" : ""
              }`}
              disabled={loading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
}

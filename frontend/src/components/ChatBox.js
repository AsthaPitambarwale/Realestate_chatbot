import React, { useState } from "react";
import { motion } from "framer-motion";

export default function ChatBox({ onSend, areas, loading }) {
  const [text, setText] = useState("");
  const example = "Analyze Wakad price trend last 3 years";

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 shadow rounded-xl p-6"
    >
      <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-3">
        💬 Ask a Query
      </h2>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={example}
        rows={3}
        className="w-full border dark:border-gray-600 rounded-lg p-3 
        dark:bg-gray-700 dark:text-gray-100"
      ></textarea>

      <div className="flex justify-between items-center mt-3">
        <button
          onClick={() => {
            onSend(text);
            setText("");
          }}
          disabled={loading}
          className="bg-indigo-600 dark:bg-indigo-700 text-white px-4 py-2 rounded-lg"
        >
          {loading ? "Processing..." : "Send"}
        </button>

        <div className="text-xs text-gray-500 dark:text-gray-400">
          Areas: {areas.slice(0, 5).join(", ")}...
        </div>
      </div>
    </motion.div>
  );
}

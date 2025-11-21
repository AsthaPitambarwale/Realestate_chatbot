import React from "react";
import { motion } from "framer-motion";

export default function Summary({ text, meta }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 shadow rounded-xl p-6"
    >
      <div className="bg-white dark:bg-gray-800 p-6 shadow rounded-xl">
        <h2 className="text-2xl font-semibold mb-3 text-gray-800 dark:text-gray-100">
          📌 Summary
        </h2>

        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          {text}
        </p>
      </div>
    </motion.div>
  );
}

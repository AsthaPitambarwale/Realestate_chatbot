import React, { useRef } from "react";
import { motion } from "framer-motion";

export default function UploadForm({ onUpload, loading }) {
  const fileRef = useRef();

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 shadow rounded-xl p-6"
    >
      <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
        📤 Upload Dataset
      </h2>

      <div
        className="border-2 border-dashed rounded-xl py-8 text-center cursor-pointer 
        hover:bg-gray-50 dark:hover:bg-gray-700 transition"
        onClick={() => fileRef.current.click()}
      >
        <p className="text-gray-500 dark:text-gray-300">
          Click to choose an Excel file (.xlsx)
        </p>
      </div>

      <input
        ref={fileRef}
        type="file"
        accept=".xlsx,.xls"
        className="hidden"
        onChange={(e) => onUpload(e.target.files[0])}
      />

      <button
        onClick={() => fileRef.current.click()}
        disabled={loading}
        className="mt-4 w-full bg-green-600 dark:bg-green-700 text-white py-2 rounded-lg"
      >
        {loading ? "Uploading..." : "Choose File"}
      </button>
    </motion.div>
  );
}

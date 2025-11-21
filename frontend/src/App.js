import React, { useState, useEffect } from "react";
import api from "./api";
import UploadForm from "./components/UploadForm";
import ChatBox from "./components/ChatBox";
import Summary from "./components/Summary";
import ChartComponent from "./components/ChartComponent";
import TableComponent from "./components/TableComponent";
import Sidebar from "./components/Sidebar";
import SkeletonCard from "./components/SkeletonCard";
import AIHelpButton from "./components/AIHelpButton";
import toast, { Toaster } from "react-hot-toast";

export default function App() {
  const [areas, setAreas] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dark, setDark] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  useEffect(() => {
    api.get("/areas/").then((res) => {
      setAreas(res.data.areas || []);
    });
  }, []);

  async function handleUpload(file) {
    if (!file) return toast.error("Select a file");

    setLoading(true);
    try {
      const form = new FormData();
      form.append("file", file);

      await api.post("/upload/", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const r = await api.get("/areas/");
      setAreas(r.data.areas);
      toast.success("Dataset uploaded!");
    } finally {
      setLoading(false);
    }
  }

  async function sendQuery(q) {
    setLoading(true);
    try {
      const res = await api.post("/query/", { query: q });
      setResult(res.data);
    } catch {
      toast.error("Query failed");
    }
    setLoading(false);
  }

  return (
    <div className="flex">
      <Sidebar dark={dark} toggleDark={() => setDark(!dark)} />

      <div className="md:ml-64 p-6 w-full min-h-screen">
        <Toaster position="top-center" />

        <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-8 text-center">
          🏡 Real Estate Analytics Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* LEFT PANEL */}
          <div className="space-y-6">
            <UploadForm onUpload={handleUpload} loading={loading} />
            <ChatBox onSend={sendQuery} loading={loading} areas={areas} />
          </div>

          {/* RIGHT PANEL */}
          <div className="md:col-span-2 space-y-6">
            {loading && (
              <>
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
              </>
            )}

            {!loading && !result && (
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow text-center text-gray-500 dark:text-gray-300">
                Upload dataset & ask a query to view analysis.
              </div>
            )}

            {result && (
              <>
                <Summary text={result.summary} meta={result} />
                <ChartComponent chart={result.chart} />
                <TableComponent table={result.table} />
              </>
            )}
          </div>
        </div>

        <AIHelpButton />
      </div>
    </div>
  );
}

import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

// Register chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function TrendChart({ chart }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    // Check for valid chart data
    if (!chart || !chart.labels || chart.labels.length === 0) return;

    // Map datasets dynamically from backend
    const datasets = (chart.datasets || []).map((d, idx) => ({
      label: d.label,
      data: d.data,
      borderColor: `hsl(${(idx * 60) % 360}, 70%, 45%)`,
      backgroundColor: `hsla(${(idx * 60) % 360}, 70%, 45%, 0.15)`,
      borderWidth: 2,
      tension: 0.4,
      fill: true,
      pointRadius: 3,
    }));

    setChartData({
      labels: chart.labels,
      datasets: datasets,
    });
  }, [chart]);

  if (!chartData) return null;

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-2xl p-6 overflow-auto">
      <h2 className="text-xl font-semibold mb-4">📈 Trends</h2>
      <Line
        data={chartData}
        options={{
          responsive: true,
          plugins: {
            legend: {
              position: "top",
              labels: {
                usePointStyle: true,
              },
            },
            tooltip: {
              mode: "index",
              intersect: false,
            },
          },
          interaction: {
            mode: "nearest",
            axis: "x",
            intersect: false,
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: { color: "#4B5563" },
            },
            x: {
              ticks: { color: "#4B5563" },
            },
          },
        }}
      />
    </div>
  );
}

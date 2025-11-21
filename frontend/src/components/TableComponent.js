import React from "react";

export default function TableComponent({ table }) {
  if (!table || table.length === 0) return null;

  const headers = Object.keys(table[0]);

  const downloadCSV = () => {
    if (!table || table.length === 0) return;

    const headers = Object.keys(table[0]).join(",");

    const rows = table
      .map((row) =>
        Object.values(row)
          .map((value) => `"${String(value).replace(/"/g, '""')}"`)
          .join(",")
      )
      .join("\n");

    const csvContent = headers + "\n" + rows;
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "table_data.csv";
    link.click();
  };

  const downloadExcel = () => {
    if (!table || table.length === 0) return;

    const tableHtml = `
      <table>
        <thead>
          <tr>
            ${headers.map((h) => `<th>${h}</th>`).join("")}
          </tr>
        </thead>
        <tbody>
          ${table
            .map(
              (row) =>
                `<tr>${headers
                  .map((h) => `<td>${String(row[h]).replace(/"/g, '""')}</td>`)
                  .join("")}</tr>`
            )
            .join("")}
        </tbody>
      </table>
    `;

    const blob = new Blob([tableHtml], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "table_data.xlsx";
    link.click();
  };

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-2xl p-6 overflow-auto">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">
        📊 Data Table
      </h2>

      <div className="flex mb-4">
        <button
          onClick={downloadCSV}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          ⬇ Download CSV
        </button>
      </div>

      <table className="min-w-full border border-gray-200 dark:border-gray-700 rounded-lg">
        <thead className="bg-gray-100 dark:bg-gray-700">
          <tr>
            {headers.map((h) => (
              <th
                key={h}
                className="p-2 text-sm text-gray-700 dark:text-gray-200 border-b border-gray-200 dark:border-gray-600"
              >
                {h.toUpperCase()}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {table.map((row, i) => (
            <tr
              key={i}
              className={
                i % 2 === 0
                  ? "bg-white dark:bg-gray-900"
                  : "bg-gray-50 dark:bg-gray-800"
              }
            >
              {headers.map((h) => (
                <td
                  key={h}
                  className="p-2 text-gray-800 dark:text-gray-200 border-b border-gray-200 dark:border-gray-700"
                >
                  {String(row[h])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

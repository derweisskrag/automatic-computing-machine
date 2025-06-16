"use client";

import type { PredictionRequest, PythonModelResponseType } from "@/common_types/wind_data";
import { useState, useEffect } from "react";

export default function PredictionForm() {
   const [data, setData] = useState<PredictionRequest>(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("predictionFormData");
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch {
          console.error("Failed to parse localStorage data.");
        }
      }
    }
    return {
      Wind_Speed: 0,
      Wind_Gust: 0,
      Wind_Direction: 0,
      Temperature: 0,
      Humidity: 0,
      Precipitation: 0,
      Pressure: 0,
      Cloud_Cover: 0,
      Solar_Radiation: 0,
      Hour_of_Day: 0,
      Day_of_Week: 0,
      Month: 0,
    };
  });

  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [prediction, setPrediction] = useState<PythonModelResponseType | null>(null);


  useEffect(() => {
    localStorage.setItem("predictionFormData", JSON.stringify(data));
  }, [data]);


  const onSubmit = async (data: PredictionRequest) => {
    try {
      const result = await fetch(`/api/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!result.ok) throw new Error("Network error");

      const json = await result.json();

      setPrediction(json);
      setIsModalOpen(true);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(data);
  };

  return (
    <section className="max-w-2xl mx-auto p-4 bg-white shadow rounded">
      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {Object.keys(data).map((key) => (
          <div key={key} className="flex flex-col">
            <label htmlFor={key} className="text-sm font-medium capitalize">
              {key.replace(/_/g, " ")}
            </label>
            <input
              type="number"
              step="any"
              min="0"
              id={key}
              name={key}
              className="border border-gray-300 rounded p-2"
              value={data[key as keyof typeof data]}
              onChange={(e) => {
                const val = Number(e.target.value);
                setData({
                  ...data,
                  [key]: isNaN(val) ? 0 : val,
                });
              }}
            />
          </div>
        ))}
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Predict
        </button>
      </form>


      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-sm w-full">
            <h2 className="text-xl font-semibold mb-4">Prediction Result</h2>
            <div className="text-gray-700">
              <div className="text-gray-700 mb-2">Here are your model predictions:</div>
                <table className="w-full text-sm text-left text-gray-700">
                <thead>
                    <tr>
                    <th className="font-semibold pb-2">Model</th>
                    <th className="font-semibold pb-2">Prediction</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <td>XGBoost</td>
                    <td className="font-bold">{prediction?.xgboost_prediction?.toFixed(2)}</td>
                    </tr>
                    <tr>
                    <td>Random Forest</td>
                    <td className="font-bold">{prediction?.random_forest_prediction?.toFixed(2)}</td>
                    </tr>
                    <tr>
                    <td>Linear Regression</td>
                    <td className="font-bold">{prediction?.linear_regression_prediction?.toFixed(2)}</td>
                    </tr>
                    <tr>
                    <td>Gradient Boosting</td>
                    <td className="font-bold">{prediction?.gradient_boosting_prediction?.toFixed(2)}</td>
                    </tr>
                </tbody>
                </table>
            </div>
            <button
              onClick={() => setIsModalOpen(false)}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </section>
  );
}
"use client";

import { useEffect, useState } from "react";

interface TemperatureReading {
  temperature: number;
  timestamp: string;
  sensor?: string;
}

export default function Home() {
  const [readings, setReadings] = useState<TemperatureReading[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch temperature data
    const fetchData = async () => {
      try {
        const response = await fetch("/api/temperature");
        const data = await response.json();
        setReadings(data.readings || []);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching temperature data:", error);
        setLoading(false);
      }
    };

    // Initial fetch
    fetchData();

    // Refresh every 5 seconds
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  const latestReading = readings[0];
  const averageTemp =
    readings.length > 0
      ? readings.reduce((sum, r) => sum + r.temperature, 0) / readings.length
      : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🌡️ Raspberry Pi Temperature Monitor
          </h1>
          <p className="text-gray-600">Real-time temperature readings</p>
        </header>

        {loading ? (
          <div className="text-center text-gray-600">Loading...</div>
        ) : (
          <>
            {/* Current Temperature Card */}
            <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">
                Current Temperature
              </h2>
              {latestReading ? (
                <div className="text-center">
                  <div className="text-6xl font-bold text-indigo-600 mb-2">
                    {latestReading.temperature.toFixed(1)}°C
                  </div>
                  <div className="text-sm text-gray-500">
                    Last updated:{" "}
                    {new Date(latestReading.timestamp).toLocaleString()}
                  </div>
                  {latestReading.sensor && (
                    <div className="text-sm text-gray-500 mt-1">
                      Sensor: {latestReading.sensor}
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center text-gray-500 py-8">
                  No temperature data available yet.
                  <br />
                  Waiting for Raspberry Pi to send data...
                </div>
              )}
            </div>

            {/* Statistics */}
            {readings.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-sm font-semibold text-gray-600 mb-2">
                    Average
                  </h3>
                  <div className="text-3xl font-bold text-blue-600">
                    {averageTemp.toFixed(1)}°C
                  </div>
                </div>
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-sm font-semibold text-gray-600 mb-2">
                    Maximum
                  </h3>
                  <div className="text-3xl font-bold text-red-600">
                    {Math.max(...readings.map((r) => r.temperature)).toFixed(
                      1
                    )}
                    °C
                  </div>
                </div>
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-sm font-semibold text-gray-600 mb-2">
                    Minimum
                  </h3>
                  <div className="text-3xl font-bold text-green-600">
                    {Math.min(...readings.map((r) => r.temperature)).toFixed(
                      1
                    )}
                    °C
                  </div>
                </div>
              </div>
            )}

            {/* Recent Readings */}
            {readings.length > 0 && (
              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h2 className="text-xl font-semibold text-gray-700 mb-4">
                  Recent Readings
                </h2>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 text-gray-600 font-semibold">
                          Temperature
                        </th>
                        <th className="text-left py-3 px-4 text-gray-600 font-semibold">
                          Time
                        </th>
                        <th className="text-left py-3 px-4 text-gray-600 font-semibold">
                          Sensor
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {readings.slice(0, 10).map((reading, index) => (
                        <tr
                          key={index}
                          className="border-b border-gray-100 hover:bg-gray-50"
                        >
                          <td className="py-3 px-4 font-semibold text-indigo-600">
                            {reading.temperature.toFixed(1)}°C
                          </td>
                          <td className="py-3 px-4 text-gray-600">
                            {new Date(reading.timestamp).toLocaleTimeString()}
                          </td>
                          <td className="py-3 px-4 text-gray-600">
                            {reading.sensor || "default"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

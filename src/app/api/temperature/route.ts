import { NextResponse } from "next/server";

// Store temperature readings in memory (in production, use a database)
let temperatureReadings: Array<{
  temperature: number;
  timestamp: string;
  sensor?: string;
}> = [];

// Maximum number of readings to keep
const MAX_READINGS = 100;

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { temperature, sensor } = body;

    if (typeof temperature !== "number") {
      return NextResponse.json(
        { error: "Temperature must be a number" },
        { status: 400 }
      );
    }

    // Add new reading
    const reading = {
      temperature,
      timestamp: new Date().toISOString(),
      sensor: sensor || "default",
    };

    temperatureReadings.unshift(reading);

    // Keep only the latest readings
    if (temperatureReadings.length > MAX_READINGS) {
      temperatureReadings = temperatureReadings.slice(0, MAX_READINGS);
    }

    return NextResponse.json({
      success: true,
      reading,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Invalid request" },
      { status: 400 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    readings: temperatureReadings,
    count: temperatureReadings.length,
  });
}

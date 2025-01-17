import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    // Get the URL object from the incoming request
    const { searchParams } = new URL(request.url);
    const timePeriod = searchParams.get('time_period');
    
    // Construct the backend URL with the time_period parameter
    const backendUrl = `http://localhost:5001/daily_steps?time_period=${timePeriod}`;
    console.log('Fetching from backend:', backendUrl);

    const response = await fetch(backendUrl, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    // console.log(response)
    // Get the text response first
    const rawText = await response.text();
    // console.log(rawText)
    
    // Replace NaN with null in the string before parsing
    const sanitizedText = rawText.replace(/:\s*NaN/g, ':null');
    
    // Parse the sanitized JSON
    const data = JSON.parse(sanitizedText);

    // Clean the data
    const cleanData = data.map((item: any) => ({
      date: item.date,
      distance: item.distance ?? 0,
      step_goal: item.step_goal ?? 10000,
      total_steps: item.total_steps ?? 0,
    }));

    return NextResponse.json(cleanData);
    
  } catch (error) {
    console.error('Error fetching step data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch step data' },
      { status: 500 }
    );
  }
}
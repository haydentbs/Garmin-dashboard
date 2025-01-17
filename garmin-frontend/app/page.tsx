'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import StepChart from '@/components/StepChart';
import DataControls, { TimeRange, AggregationType } from '@/components/DataControls';
import styles from './page.module.css';
import { StepData } from '@/types/steps';
import ActivityChart from '@/components/ActivityChart'

export default function Home() {
  const [stepData, setStepData] = useState<StepData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<TimeRange>('7days');
  const [aggregationType, setAggregationType] = useState<AggregationType>('daily');

  useEffect(() => {
    const fetchStepData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(
          `/api/dailySteps?time_period=${timeRange}`
        );
        console.log('Time Period: ' + timeRange)
        
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
        console.log(data)
        setStepData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchStepData();
    
  }, [timeRange, aggregationType]);

  if (isLoading) {
    return (
      <div className={styles.wrapper}>
        <Header />
        <main className={styles.main}>
          <div className={styles.loading}>Loading...</div>
        </main>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.wrapper}>
        <Header />
        <main className={styles.main}>
          <div className={styles.error}>Error: {error}</div>
        </main>
      </div>
    );
  }

  const activityData = [
    {
      date: "2024-03-01",
      activities: {
        running: 45,  // minutes
        cycling: 120,
        gym: 60
      }
    },
    // ... more days
  ];

  return (
    <div className={styles.wrapper}>
      <Header />
      <main className={styles.main}>
        <DataControls
          selectedRange={timeRange}
          selectedAggregation={aggregationType}
          onTimeRangeChange={setTimeRange}
          onAggregationChange={setAggregationType}
        />
        <div className={styles.chartContainer}>
          <StepChart data={stepData} />
          <ActivityChart data={activityData} />
          
        </div>
      </main>
    </div>
  );
}
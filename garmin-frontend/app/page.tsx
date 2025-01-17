'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import StepChart from '@/components/StepChart';
import DataControls, { TimeRange, AggregationType } from '@/components/DataControls';
import styles from './page.module.css';
import { StepData } from '@/types/steps';

export default function Home() {
  const [stepData, setStepData] = useState<StepData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<TimeRange>('30days');
  const [aggregationType, setAggregationType] = useState<AggregationType>('daily');

  useEffect(() => {
    const fetchStepData = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(
          `/api/daily_steps?range=${timeRange}&aggregation=${aggregationType}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
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
        </div>
      </main>
    </div>
  );
}
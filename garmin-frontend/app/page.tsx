'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import StepChart from '@/components/StepChart';
import DataControls, { TimeRange, AggregationType } from '@/components/DataControls';
import styles from './page.module.css';
import { StepData } from '@/types/steps';
import { ActivityData } from '@/types/activity';
import ActivityChart from '@/components/ActivityChart'
import { fetchStepData, fetchActivityData } from '@/services/dataService';

export default function Home() {
  const [stepData, setStepData] = useState<StepData[]>([]);
  const [activityData, setActivityData] = useState<ActivityData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState<TimeRange>('7days');
  const [aggregationType, setAggregationType] = useState<AggregationType>('daily');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [steps, activities] = await Promise.all([
          fetchStepData(timeRange),
          fetchActivityData(timeRange)
        ]);
        
        setStepData(steps);
        setActivityData(activities);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
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
          <ActivityChart data={activityData} />
        </div>
      </main>
    </div>
  );
}
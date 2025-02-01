import { StepData } from '@/types/steps';
import { ActivityData } from '@/types/activity';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

export const fetchStepData = async (timeRange: string): Promise<StepData[]> => {
  const response = await fetch(`${API_BASE_URL}/daily_steps?time_period=${timeRange}`);
  console.log('Step Data: ', response)
  
  if (!response.ok) {
    throw new Error('Failed to fetch step data');
  }
  
  return await response.json();
};

export const fetchActivityData = async (timeRange: string): Promise<ActivityData[]> => {
  const response = await fetch(`${API_BASE_URL}/activity_list?time_period=${timeRange}`);
  console.log('Activity Data', response)
  
  if (!response.ok) {
    throw new Error('Failed to fetch activity data');
  }
  
  return await response.json();
};
import { StepData } from '@/types/steps';
import { ActivityData } from '@/types/activity';


export const fetchStepData = async (timeRange: string): Promise<StepData[]> => {
  const response = await fetch(`/api/dailySteps?time_period=${timeRange}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch step data');
  }
  
  return await response.json();
};

export const fetchActivityData = async (timeRange: string): Promise<ActivityData[]> => {
  const response = await fetch(`/api/activities?time_period=${timeRange}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch activity data');
  }
  
  return await response.json();
};
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    TooltipItem,
  } from 'chart.js';
  import { Bar } from 'react-chartjs-2';
  import { useState } from 'react';
  import styles from './ActivityChart.module.css';
  import { ActivityData } from '@/types/activity';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );
  
  // Define activity types and their colors
  const ACTIVITIES = {
    running: { label: 'Running', color: 'rgba(75, 192, 192, 0.8)', borderColor: 'rgb(75, 192, 192)' },
    cycling: { label: 'Cycling', color: 'rgba(255, 99, 132, 0.8)', borderColor: 'rgb(255, 99, 132)' },
    strength_training: { label: 'Gym', color: 'rgba(54, 162, 235, 0.8)', borderColor: 'rgb(54, 162, 235)' },
  };
  
  // interface ActivityData {
  //   date: string;
  //   activities: {
  //     running?: number;
  //     cycling?: number;
  //     gym?: number;
  //   };
  // }

  // export interface ActivityData {
  //   actitivyName: string;
  //   activityTypeName: string;
  //   elapsedDuration: number;
  //   startTimeGMT: string;
  // }
  
  interface Props {
    data: ActivityData[];
  }
  
  // Helper function to process the activity data
  const processActivityData = (activities: ActivityData[]) => {
    const dailyActivities = activities.reduce((acc: { [key: string]: { [key: string]: number } }, activity) => {
      // Format date to YYYY-MM-DD for grouping
      const date = new Date(activity.startTimeGMT).toISOString().split('T')[0];
      
      // Initialize date entry if it doesn't exist
      if (!acc[date]) {
        acc[date] = {};
      }
      
      // Convert activityTypeName to lowercase for consistency
      const activityType = activity.activityTypeName.toLowerCase();
      
      // Add duration in minutes (assuming elapsedDuration is in seconds)
      acc[date][activityType] = (acc[date][activityType] || 0) + activity.elapsedDuration / 60;
      
      return acc;
    }, {});

    // Convert to array format
    return Object.entries(dailyActivities).map(([date, activities]) => ({
      date,
      activities
    }));
  };

  const ActivityChart: React.FC<Props> = ({ data }) => {
    const [selectedActivities, setSelectedActivities] = useState(Object.keys(ACTIVITIES));
  
    // Process the raw activity data
    const processedData = processActivityData(data);

    const toggleActivity = (activity: string) => {
      setSelectedActivities(current => 
        current.includes(activity)
          ? current.filter(a => a !== activity)
          : [...current, activity]
      );
    };
  
    const chartData = {
      labels: processedData.map(d => new Date(d.date).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })),
      datasets: selectedActivities.map(activity => ({
        label: ACTIVITIES[activity as keyof typeof ACTIVITIES].label,
        data: processedData.map(d => d.activities[activity] || 0),
        backgroundColor: ACTIVITIES[activity as keyof typeof ACTIVITIES].color,
        borderColor: ACTIVITIES[activity as keyof typeof ACTIVITIES].borderColor,
        borderWidth: 1,
      })),
    };
  
    const options = {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'Daily Activity Duration',
        },
        tooltip: {
          callbacks: {
            label: (context: TooltipItem<'bar'>) => {
              const minutes = context.raw as number;
              const hours = Math.floor(minutes / 60);
              const remainingMinutes = minutes % 60;
              return `${context.dataset.label}: ${hours}h ${remainingMinutes}m`;
            },
          },
        },
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Minutes',
          },
        },
      },
    };
  
    return (
      <div className={styles.chartContainer}>
        <div className={styles.toggles}>
          {Object.entries(ACTIVITIES).map(([key, value]) => (
            <label key={key} className={styles.toggle}>
              <input
                type="checkbox"
                checked={selectedActivities.includes(key)}
                onChange={() => toggleActivity(key)}
              />
              <span 
                className={styles.activityLabel}
                style={{ backgroundColor: value.color }}
              >
                {value.label}
              </span>
            </label>
          ))}
        </div>
        <Bar data={chartData} options={options} />
      </div>
    );
  };
  
  export default ActivityChart;
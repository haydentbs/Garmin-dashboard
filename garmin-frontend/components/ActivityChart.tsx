import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  import { Bar } from 'react-chartjs-2';
  import { useState } from 'react';
  import styles from './ActivityChart.module.css';
  
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
    gym: { label: 'Gym', color: 'rgba(54, 162, 235, 0.8)', borderColor: 'rgb(54, 162, 235)' },
  };
  
  interface ActivityData {
    date: string;
    activities: {
      running?: number;
      cycling?: number;
      gym?: number;
    };
  }
  
  interface Props {
    data: ActivityData[];
  }
  
  const ActivityChart: React.FC<Props> = ({ data }) => {
    const [selectedActivities, setSelectedActivities] = useState(Object.keys(ACTIVITIES));
  
    const toggleActivity = (activity: string) => {
      setSelectedActivities(current => 
        current.includes(activity)
          ? current.filter(a => a !== activity)
          : [...current, activity]
      );
    };
  
    const chartData = {
      labels: data.map(d => new Date(d.date).toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      })),
      datasets: selectedActivities.map(activity => ({
        label: ACTIVITIES[activity as keyof typeof ACTIVITIES].label,
        data: data.map(d => d.activities[activity as keyof typeof ACTIVITIES] || 0),
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
            label: (context: any) => {
              const minutes = context.raw;
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
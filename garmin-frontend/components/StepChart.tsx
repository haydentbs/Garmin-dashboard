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
import { StepData } from '@/types/steps';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  data: StepData[];
}

const StepChart: React.FC<Props> = ({ data }) => {
  const chartData = {
    labels: data.map(d => new Date(d.date).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })),
    datasets: [
      {
        label: 'Steps',
        data: data.map(d => d.total_steps),
        backgroundColor: data.map(d => 
          d.total_steps >= d.step_goal ? 'rgba(75, 192, 192, 0.8)' : 'rgba(255, 159, 64, 0.8)'
        ),
        borderColor: data.map(d => 
          d.total_steps >= d.step_goal ? 'rgb(75, 192, 192)' : 'rgb(255, 159, 64)'
        ),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Daily Steps',
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const dataPoint = data[context.dataIndex];
            return [
              `Steps: ${dataPoint.total_steps.toLocaleString()}`,
              `Goal: ${dataPoint.step_goal.toLocaleString()}`,
              `Distance: ${dataPoint.distance.toFixed(1)}m`,
            ];
          },
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
};

export default StepChart;
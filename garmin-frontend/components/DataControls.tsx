import styles from './DataControls.module.css';
import { FaCalendar, FaChartLine } from 'react-icons/fa';

export type TimeRange = '7days' | '30days' | '90days' | 'year';
export type AggregationType = 'daily' | 'weekly' | 'monthly';

interface Props {
  onTimeRangeChange: (range: TimeRange) => void;
  onAggregationChange: (type: AggregationType) => void;
  selectedRange: TimeRange;
  selectedAggregation: AggregationType;
}

const DataControls: React.FC<Props> = ({
  onTimeRangeChange,
  onAggregationChange,
  selectedRange,
  selectedAggregation,
}) => {
  return (
    <div className={styles.controls}>
      <div className={styles.controlGroup}>
        <FaCalendar className={styles.icon} />
        <select 
          value={selectedRange}
          onChange={(e) => onTimeRangeChange(e.target.value as TimeRange)}
          className={styles.select}
        >
          <option value="7days">Last 7 Days</option>
          <option value="30days">Last 30 Days</option>
          <option value="90days">Last 90 Days</option>
          <option value="year">Last Year</option>
        </select>
      </div>

      <div className={styles.controlGroup}>
        <FaChartLine className={styles.icon} />
        <select 
          value={selectedAggregation}
          onChange={(e) => onAggregationChange(e.target.value as AggregationType)}
          className={styles.select}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly Average</option>
          <option value="monthly">Monthly Average</option>
        </select>
      </div>
    </div>
  );
};

export default DataControls;
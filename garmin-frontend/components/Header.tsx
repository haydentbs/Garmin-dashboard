import styles from './Header.module.css';
import { FaRunning, FaChartBar } from 'react-icons/fa';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <div className={styles.logoSection}>
          <FaRunning className={styles.icon} />
          <h1 className={styles.title}>
            Garmin Analytics
            <span className={styles.subtitle}>Daily Activity Dashboard</span>
          </h1>
        </div>
        <div className={styles.statsSection}>
          <div className={styles.statCard}>
            <FaChartBar className={styles.statIcon} />
            <span className={styles.statLabel}>Activity Tracker</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
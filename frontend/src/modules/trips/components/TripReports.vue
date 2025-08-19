<template>
  <div class="trip-reports">
    <div class="section-header">
      <h3>
        <i class="fas fa-chart-line"></i>
        Reports & Analytics
      </h3>
    </div>

    <!-- Report Options Grid -->
    <div class="reports-grid">
      
      <!-- Passenger Reports -->
      <div class="report-section">
        <h4>
          <i class="fas fa-users"></i>
          Passenger Reports
        </h4>
        <div class="report-actions">
          <button @click="generateReport('passenger-list')" class="btn btn-primary">
            <i class="fas fa-list"></i>
            Passenger List
          </button>
          <button @click="generateReport('rooming-list')" class="btn btn-info">
            <i class="fas fa-bed"></i>
            Rooming List
          </button>
          <button @click="generateReport('special-needs')" class="btn btn-warning">
            <i class="fas fa-heartbeat"></i>
            Special Needs
          </button>
        </div>
      </div>

      <!-- Financial Reports -->
      <div class="report-section">
        <h4>
          <i class="fas fa-dollar-sign"></i>
          Financial Reports
        </h4>
        <div class="report-actions">
          <button @click="generateReport('financial-summary')" class="btn btn-success">
            <i class="fas fa-chart-pie"></i>
            Financial Summary
          </button>
          <button @click="generateReport('payment-status')" class="btn btn-info">
            <i class="fas fa-credit-card"></i>
            Payment Status
          </button>
          <button @click="generateReport('commission-report')" class="btn btn-warning">
            <i class="fas fa-percent"></i>
            Commission Report
          </button>
        </div>
      </div>

      <!-- Export Options -->
      <div class="report-section">
        <h4>
          <i class="fas fa-download"></i>
          Export Options
        </h4>
        <div class="report-actions">
          <button @click="exportData('excel')" class="btn btn-success">
            <i class="fas fa-file-excel"></i>
            Excel Export
          </button>
          <button @click="exportData('pdf')" class="btn btn-danger">
            <i class="fas fa-file-pdf"></i>
            PDF Export
          </button>
          <button @click="exportData('csv')" class="btn btn-secondary">
            <i class="fas fa-file-csv"></i>
            CSV Export
          </button>
        </div>
      </div>

      <!-- Email Reports -->
      <div class="report-section">
        <h4>
          <i class="fas fa-envelope"></i>
          Email Reports
        </h4>
        <div class="report-actions">
          <button @click="sendEmail('weekly-report')" class="btn btn-primary">
            <i class="fas fa-calendar-week"></i>
            Weekly Report
          </button>
          <button @click="sendEmail('coordinator-update')" class="btn btn-info">
            <i class="fas fa-user-tie"></i>
            Coordinator Update
          </button>
          <button @click="sendEmail('custom-report')" class="btn btn-warning">
            <i class="fas fa-envelope-open-text"></i>
            Custom Report
          </button>
        </div>
      </div>

    </div>

    <!-- Quick Stats Summary -->
    <div class="stats-summary">
      <h4>
        <i class="fas fa-tachometer-alt"></i>
        Quick Statistics
      </h4>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon passengers">
            <i class="fas fa-users"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ tripData?.passenger_count || 0 }}</div>
            <div class="stat-label">Total Passengers</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon revenue">
            <i class="fas fa-dollar-sign"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">${{ formatCurrency(tripData?.total_cost) }}</div>
            <div class="stat-label">Total Revenue</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon completion">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ calculateCompletion() }}%</div>
            <div class="stat-label">Completion</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon payments">
            <i class="fas fa-credit-card"></i>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ getPaymentStatusCount() }}</div>
            <div class="stat-label">Paid in Full</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity">
      <h4>
        <i class="fas fa-history"></i>
        Recent Activity
      </h4>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon" :class="activity.type">
            <i :class="activity.icon"></i>
          </div>
          <div class="activity-content">
            <div class="activity-description">{{ activity.description }}</div>
            <div class="activity-time">{{ formatDate(activity.timestamp) }}</div>
          </div>
        </div>
        
        <div v-if="recentActivities.length === 0" class="no-activity">
          <i class="fas fa-info-circle"></i>
          <p>No recent activity to display.</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  tripId: [String, Number],
  tripData: { type: Object, default: () => ({}) }
})

// Mock data for demonstration
const recentActivities = ref([
  {
    id: 1,
    type: 'payment',
    icon: 'fas fa-dollar-sign',
    description: 'Payment received from John Doe - $500.00',
    timestamp: new Date().toISOString()
  },
  {
    id: 2,
    type: 'passenger',
    icon: 'fas fa-user-plus',
    description: 'New passenger registered: Jane Smith',
    timestamp: new Date(Date.now() - 86400000).toISOString()
  },
  {
    id: 3,
    type: 'email',
    icon: 'fas fa-envelope',
    description: 'Welcome email sent to group leader',
    timestamp: new Date(Date.now() - 172800000).toISOString()
  }
])

const formatCurrency = (amount) => {
  return parseFloat(amount || 0).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const calculateCompletion = () => {
  // Mock calculation - would be based on actual trip milestones
  return 75
}

const getPaymentStatusCount = () => {
  // Mock count - would be based on actual passenger payment data
  return 12
}

const generateReport = (reportType) => {
  console.log('Generating report:', reportType)
  // Integrate with report.php functionality
}

const exportData = (format) => {
  console.log('Exporting data as:', format)
  // Integrate with pilgrimage_export.php functionality
}

const sendEmail = (emailType) => {
  console.log('Sending email:', emailType)
  // Integrate with email sending functionality
}
</script>

<style scoped>
.trip-reports {
  padding: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f8f9fa;
}

.section-header h3,
.section-header h4 {
  margin: 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header i {
  color: #667eea;
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.report-section {
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s ease;
}

.report-section:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.report-section h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
}

.report-section h4 i {
  color: #667eea;
}

.report-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stats-summary,
.recent-activity {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 30px;
}

.stats-summary h4,
.recent-activity h4 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.stats-summary h4 i,
.recent-activity h4 i {
  color: #667eea;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.stat-icon.passengers {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon.revenue {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.stat-icon.completion {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
}

.stat-icon.payments {
  background: linear-gradient(135deg, #17a2b8, #6f42c1);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 14px;
  font-weight: 500;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  background: white;
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: white;
}

.activity-icon.payment {
  background: #28a745;
}

.activity-icon.passenger {
  background: #667eea;
}

.activity-icon.email {
  background: #17a2b8;
}

.activity-content {
  flex: 1;
}

.activity-description {
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 4px;
}

.activity-time {
  color: #7f8c8d;
  font-size: 14px;
}

.no-activity {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
}

.no-activity i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-activity p {
  margin: 0;
  font-style: italic;
}

/* Button Styles */
.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
  transform: translateY(-1px);
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-info:hover {
  background: #138496;
  transform: translateY(-1px);
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .trip-reports {
    padding: 20px;
  }
  
  .reports-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .activity-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
}

@media (max-width: 576px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .report-actions {
    gap: 8px;
  }
  
  .btn {
    padding: 8px 14px;
    font-size: 13px;
  }
}
</style>

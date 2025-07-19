<template>
  <div class="workflow-status-container">
    <div class="workflow-steps">
      <div 
        v-for="(step, index) in workflowSteps" 
        :key="step.id"
        class="workflow-step"
        :class="getStepClass(step.id)"
      >
        <!-- Step circle with number -->
        <div class="step-circle">
          <span class="step-number">{{ index + 1 }}</span>
        </div>
        
        <!-- Step label -->
        <div class="step-label">
          {{ step.label }}
        </div>
        
        <!-- Connector line (not for last step) -->
        <div 
          v-if="index < workflowSteps.length - 1" 
          class="step-connector"
          :class="{ 'active': isStepCompleted(workflowSteps[index + 1].id) }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentStatus: {
    type: [Number, String],
    default: 10
  },
  size: {
    type: String,
    default: 'normal', // 'small', 'normal', 'large'
    validator: (value) => ['small', 'normal', 'large'].includes(value)
  }
})

const workflowSteps = [
  { id: 10, label: 'Itinerary Created' },
  { id: 20, label: 'Send to Priest' },
  { id: 30, label: 'Sends interest back' },
  { id: 40, label: 'Send a quote w/ prices' },
  { id: 50, label: 'Priest approves & sends back' },
  { id: 60, label: 'Create marketing' },
  { id: 70, label: 'Upload marketing' },
  { id: 80, label: 'Send back to Priest via DocuSign' },
  { id: 90, label: 'Receive back approval' }
]

const currentStatusNumber = computed(() => {
  return Number(props.currentStatus) || 10
})

function getStepClass(stepId) {
  const current = currentStatusNumber.value
  
  if (stepId === current) {
    return 'current'
  } else if (stepId < current) {
    return 'completed'
  } else {
    return 'pending'
  }
}

function isStepCompleted(stepId) {
  return stepId <= currentStatusNumber.value
}
</script>

<style scoped>
.workflow-status-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px 20px 10px 20px;
  border: 1px solid #dee2e6;
}

.workflow-steps {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  position: relative;
  flex-wrap: nowrap;
  gap: 0;
}

.workflow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
  min-width: 0;
}

.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 12px;
  margin-bottom: 8px;
  position: relative;
  z-index: 2;
  transition: all 0.3s ease;
}

.step-number {
  color: white;
}

.step-label {
  font-size: 11px;
  text-align: center;
  max-width: 80px;
  line-height: 1.2;
  font-weight: 500;
}

.step-connector {
  position: absolute;
  top: 15px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: #dee2e6;
  z-index: 1;
  transition: background-color 0.3s ease;
}

.step-connector.active {
  background: #9a9898;
}

/* Step states */
.workflow-step.completed .step-circle {
  background: #343a75;
  border: 2px solid #5072a7;
}

.workflow-step.current .step-circle {
  background: #3fa066;
  border: 2px solid #3dc68d;
  box-shadow: 0 0 0 3px rgba(0, 60, 9, 0.3);
}

.workflow-step.pending .step-circle {
  background: #96a1aa;
  border: 2px solid #8fa0b2;
}

.workflow-step.completed .step-label {
  color: #181817;
  font-weight: 400;
}

.workflow-step.current .step-label {
  color: #0365cf;
  font-weight: 600;
  font-size: 12px;
}

.workflow-step.pending .step-label {
  color: #181817;
  font-weight: 400;
}

/* Responsive design */
@media (max-width: 768px) {
  .workflow-steps {
    flex-direction: column;
    gap: 20px;
  }
  
  .workflow-step {
    flex-direction: row;
    min-width: 100%;
    justify-content: flex-start;
  }
  
  .step-circle {
    margin-bottom: 0;
    margin-right: 15px;
  }
  
  .step-label {
    text-align: left;
    max-width: none;
    font-size: 14px;
  }
  
  .step-connector {
    display: none;
  }
  
  /* Vertical connector for mobile */
  .workflow-step:not(:last-child)::after {
    content: '';
    position: absolute;
    left: 20px;
    top: 50px;
    width: 3px;
    height: 30px;
    background: #dee2e6;
  }
  
  .workflow-step.completed:not(:last-child)::after {
    background: #a728a5;
  }
}

/* Size variations */
.workflow-status-container.small {
  padding: 15px;
}

.workflow-status-container.small .step-circle {
  width: 25px;
  height: 25px;
  font-size: 11px;
}

.workflow-status-container.small .step-label {
  font-size: 10px;
  max-width: 70px;
}

.workflow-status-container.small .step-connector {
  top: 12px;
}

.workflow-status-container.large {
  padding: 30px;
}

.workflow-status-container.large .step-circle {
  width: 35px;
  height: 35px;
  font-size: 13px;
}

.workflow-status-container.large .step-label {
  font-size: 12px;
  max-width: 90px;
}

.workflow-status-container.large .step-connector {
  top: 17px;
}
</style>

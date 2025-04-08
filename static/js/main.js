// ArtifAI - Main JavaScript functions

// Flash message functionality
function showFlashMessage(message, category = 'info') {
  const alertContainer = document.getElementById('flash-messages');
  if (!alertContainer) return;

  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${category} alert-dismissible fade show`;
  alertDiv.role = 'alert';
  
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  alertContainer.appendChild(alertDiv);
  
  // Auto-hide the alert after 5 seconds
  setTimeout(() => {
    const bsAlert = new bootstrap.Alert(alertDiv);
    bsAlert.close();
  }, 5000);
}

// Format date strings to a more readable format
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Handle form validation
function validateForm(formElement) {
  if (!formElement.checkValidity()) {
    formElement.classList.add('was-validated');
    return false;
  }
  return true;
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
  // Initialize all tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Initialize all popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function(popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
});

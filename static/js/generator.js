// ArtifAI - Image Generator functionality

document.addEventListener('DOMContentLoaded', function() {
  initializeGenerator();
});

function initializeGenerator() {
  // Get form elements
  const generatorForm = document.getElementById('generator-form');
  const promptInput = document.getElementById('prompt');
  const generateBtn = document.getElementById('generate-btn');
  const styleOptions = document.querySelectorAll('.style-option');
  const aspectRatioOptions = document.querySelectorAll('.aspect-ratio-option');
  const generatedImageContainer = document.getElementById('generated-image');
  const imageResultSection = document.getElementById('image-result-section');
  
  // Style selection
  styleOptions.forEach(option => {
    option.addEventListener('click', function() {
      // Remove selected class from all options
      styleOptions.forEach(opt => opt.classList.remove('selected'));
      // Add selected class to clicked option
      this.classList.add('selected');
      // Update hidden input
      document.getElementById('style').value = this.getAttribute('data-style');
    });
  });
  
  // Aspect ratio selection
  aspectRatioOptions.forEach(option => {
    option.addEventListener('click', function() {
      // Remove selected class from all options
      aspectRatioOptions.forEach(opt => opt.classList.remove('selected'));
      // Add selected class to clicked option
      this.classList.add('selected');
      // Update hidden input
      document.getElementById('aspect-ratio').value = this.getAttribute('data-ratio');
    });
  });
  
  // Form submission
  if (generatorForm) {
    generatorForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Validate form
      if (!promptInput.value.trim()) {
        promptInput.classList.add('is-invalid');
        return;
      }
      
      // Remove validation errors
      promptInput.classList.remove('is-invalid');
      
      // Get form data
      const style = document.getElementById('style').value;
      const aspectRatio = document.getElementById('aspect-ratio').value;
      
      // Show loading state
      generateBtn.disabled = true;
      generateBtn.classList.add('loading');
      generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm loading-spinner me-2"></span>Generating...';
      
      // Hide any previous image
      imageResultSection.classList.add('d-none');
      
      // Send request to generate image
      generateImage(promptInput.value, style, aspectRatio)
        .then(data => {
          // Reset button state
          generateBtn.disabled = false;
          generateBtn.classList.remove('loading');
          generateBtn.innerHTML = 'Generate';
          
          if (data.success) {
            // Display the generated image
            displayGeneratedImage(data.image);
          } else {
            showFlashMessage(data.error || 'Failed to generate image. Please try again.', 'danger');
          }
        })
        .catch(error => {
          console.error('Error generating image:', error);
          
          // Reset button state
          generateBtn.disabled = false;
          generateBtn.classList.remove('loading');
          generateBtn.innerHTML = 'Generate';
          
          showFlashMessage('An error occurred while generating the image. Please try again.', 'danger');
        });
    });
  }
  
  // Reset validation on input
  if (promptInput) {
    promptInput.addEventListener('input', function() {
      if (this.value.trim()) {
        this.classList.remove('is-invalid');
      }
    });
  }
}

// Generate image API call
function generateImage(prompt, style, aspectRatio) {
  return fetch('/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      prompt: prompt,
      style: style,
      aspectRatio: aspectRatio
    })
  })
  .then(response => response.json());
}

// Display the generated image
function displayGeneratedImage(image) {
  const imageResultSection = document.getElementById('image-result-section');
  const generatedImage = document.getElementById('generated-image');
  const generatedPrompt = document.getElementById('generated-prompt');
  const generatedStyle = document.getElementById('generated-style');
  const generatedTime = document.getElementById('generated-time');
  
  // Update image and metadata
  generatedImage.src = image.url;
  generatedPrompt.textContent = image.prompt;
  generatedStyle.textContent = image.style;
  generatedTime.textContent = formatDate(image.created_at);
  
  // Show the result section
  imageResultSection.classList.remove('d-none');
  
  // Scroll to the image
  setTimeout(() => {
    imageResultSection.scrollIntoView({ behavior: 'smooth' });
  }, 100);
  
  // Show success message
  showFlashMessage('Image generated successfully! You can find it in your gallery.', 'success');
}

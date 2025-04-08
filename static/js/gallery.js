// ArtifAI - Gallery functionality

document.addEventListener('DOMContentLoaded', function() {
  // Initial page load
  let currentPage = 1;
  loadImages(currentPage);
  
  // Load more button
  const loadMoreBtn = document.getElementById('load-more');
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function() {
      currentPage++;
      loadImages(currentPage, true);
    });
  }
  
  // Initialize gallery events
  initGalleryEvents();
});

// Load images from the server
function loadImages(page, append = false) {
  const galleryContainer = document.getElementById('gallery-container');
  const loadingSpinner = document.getElementById('gallery-loading');
  const loadMoreBtn = document.getElementById('load-more');
  const noImages = document.getElementById('no-images-message');
  
  if (!galleryContainer) return;
  
  loadingSpinner.classList.remove('d-none');
  
  fetch(`/api/images?page=${page}&per_page=12`)
    .then(response => response.json())
    .then(data => {
      loadingSpinner.classList.add('d-none');
      
      if (data.images.length === 0 && page === 1) {
        // No images found
        if (noImages) noImages.classList.remove('d-none');
        if (loadMoreBtn) loadMoreBtn.classList.add('d-none');
        return;
      }
      
      if (noImages) noImages.classList.add('d-none');
      
      // Check if we have more pages
      if (page >= data.pages) {
        loadMoreBtn.classList.add('d-none');
      } else {
        loadMoreBtn.classList.remove('d-none');
      }
      
      // Clear the gallery if not appending
      if (!append) {
        galleryContainer.innerHTML = '';
      }
      
      // Add new images
      data.images.forEach(image => {
        const imageCard = createImageCard(image);
        galleryContainer.appendChild(imageCard);
      });
      
      // Reinitialize events for new cards
      initGalleryEvents();
    })
    .catch(error => {
      console.error('Error loading images:', error);
      loadingSpinner.classList.add('d-none');
      showFlashMessage('Failed to load images. Please try again later.', 'danger');
    });
}

// Create an image card element
function createImageCard(image) {
  const col = document.createElement('div');
  col.className = 'col';
  
  const favoriteIcon = image.is_favorite ? 
    '<i class="fas fa-heart text-danger"></i>' : 
    '<i class="far fa-heart"></i>';
  
  col.innerHTML = `
    <div class="card h-100 image-card" data-image-id="${image.id}">
      <img src="${image.url}" class="card-img-top" alt="${image.prompt}">
      <div class="image-actions">
        <button class="btn btn-sm btn-light rounded-circle favorite-btn" data-image-id="${image.id}" data-favorite="${image.is_favorite ? 'true' : 'false'}">
          ${favoriteIcon}
        </button>
        <button class="btn btn-sm btn-danger rounded-circle delete-btn" data-image-id="${image.id}">
          <i class="fas fa-trash"></i>
        </button>
      </div>
      <div class="card-body">
        <p class="card-text prompt-text">${image.prompt}</p>
        <div class="d-flex justify-content-between align-items-center">
          <small class="text-muted">${formatDate(image.created_at)}</small>
          <span class="badge bg-primary">${image.style}</span>
        </div>
      </div>
    </div>
  `;
  
  return col;
}

// Initialize event listeners for gallery items
function initGalleryEvents() {
  // Favorite button click
  document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const imageId = this.getAttribute('data-image-id');
      const isFavorite = this.getAttribute('data-favorite') === 'true';
      
      toggleFavorite(imageId, this, isFavorite);
    });
  });
  
  // Delete button click
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const imageId = this.getAttribute('data-image-id');
      const card = this.closest('.col');
      
      if (confirm('Are you sure you want to delete this image?')) {
        deleteImage(imageId, card);
      }
    });
  });
}

// Toggle favorite status for an image
function toggleFavorite(imageId, button, currentStatus) {
  fetch(`/api/images/${imageId}/favorite`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Update button state
      button.setAttribute('data-favorite', data.is_favorite ? 'true' : 'false');
      button.innerHTML = data.is_favorite ? 
        '<i class="fas fa-heart text-danger"></i>' : 
        '<i class="far fa-heart"></i>';
    } else {
      showFlashMessage('Failed to update favorite status.', 'danger');
    }
  })
  .catch(error => {
    console.error('Error toggling favorite:', error);
    showFlashMessage('Failed to update favorite status.', 'danger');
  });
}

// Delete an image
function deleteImage(imageId, cardElement) {
  fetch(`/api/images/${imageId}`, {
    method: 'DELETE'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Remove the card from the UI with animation
      cardElement.style.opacity = '0';
      setTimeout(() => {
        cardElement.remove();
        
        // Check if there are no images left
        const galleryContainer = document.getElementById('gallery-container');
        if (!galleryContainer.children.length) {
          const noImages = document.getElementById('no-images-message');
          if (noImages) noImages.classList.remove('d-none');
          
          const loadMoreBtn = document.getElementById('load-more');
          if (loadMoreBtn) loadMoreBtn.classList.add('d-none');
        }
      }, 300);
      
      showFlashMessage('Image deleted successfully.', 'success');
    } else {
      showFlashMessage('Failed to delete image.', 'danger');
    }
  })
  .catch(error => {
    console.error('Error deleting image:', error);
    showFlashMessage('Failed to delete image.', 'danger');
  });
}

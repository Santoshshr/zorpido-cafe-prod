// Details modal population
document.querySelectorAll('.details-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
        var name = this.dataset.name || '';
        var image = this.dataset.image || '';
        var description = this.dataset.description || '';

        document.getElementById('dishDetailsTitle').innerText = name;
        var imgEl = document.getElementById('dishDetailsImage');
        if(image) {
            imgEl.src = image;
            imgEl.style.display = 'block';
        } else {
            imgEl.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800';
        }
        document.getElementById('dishDetailsDescription').innerText = description;

        var modal = new bootstrap.Modal(document.getElementById('dishDetailsModal'));
        modal.show();
    });
});


function copyPhone() {
    const phone = "+9779845910341";
    navigator.clipboard.writeText(phone);

    const status = document.getElementById("copy-status");
    status.style.display = "inline";
    setTimeout(() => { status.style.display = "none"; }, 2000);
}



/**
 * ZORPIDO hero-section  - JavaScript
 */
// Parallax effect for floating shapes
document.addEventListener('mousemove', function (e) {
  const shapes = document.querySelectorAll('.floating-shape');
  const mouseX = e.clientX;
  const mouseY = e.clientY;

  shapes.forEach((shape, index) => {
    const speed = (index + 1) * 0.02;
    const x = (mouseX * speed);
    const y = (mouseY * speed);

    if (index === 0) {
      shape.style.transform = `translate(${x}px, ${y}px)`;
    } else if (index === 1) {
      shape.style.transform = `translate(${-x * 0.75}px, ${y * 0.75}px)`;
    } else {
      shape.style.transform = `translate(${x * 0.5}px, ${-y * 0.5}px)`;
    }

    shape.style.transition = 'transform 0.3s ease-out';
  });
});

// Smooth scroll for buttons
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Scroll fade effect
window.addEventListener('scroll', function () {
  const scrollIndicator = document.querySelector('.scroll-indicator');
  if (scrollIndicator) {
    const scrollY = window.scrollY;
    scrollIndicator.style.opacity = Math.max(0, 1 - scrollY / 300);
  }
});



// featured gallery section
/**
 * ZORPIDO FEATURED SLIDER - JavaScript
 * Enhanced Image Gallery with Advanced Features
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    autoPlayInterval: 5000,
    transitionDuration: 800,
    pauseOnHover: true,
    enableKeyboard: true,
    enableTouch: true,
    enableFullscreen: true
  };

  let currentIndex = 0;
  let autoPlayTimer = null;
  let isTransitioning = false;
  let isAutoPlaying = true;

  // Initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /**
   * Initialize the featured slider
   */
  function init() {
    const carousel = document.querySelector('.zorpido-carousel');
    if (!carousel) return;

    const slides = document.querySelectorAll('.carousel-slide');
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    const progressDots = document.querySelectorAll('.progress-dot');
    const prevBtn = document.querySelector('.arrow-prev');
    const nextBtn = document.querySelector('.arrow-next');
    const autoplayBtn = document.querySelector('.autoplay-toggle');
    const images = document.querySelectorAll('.image-container');

    if (slides.length === 0) return;

    // Setup controls
    setupNavigation(slides, thumbnails, progressDots, prevBtn, nextBtn);
    setupAutoplay(slides, thumbnails, progressDots, autoplayBtn);
    setupFullscreen(slides, images);
    
    if (CONFIG.enableKeyboard) setupKeyboard(slides, thumbnails, progressDots);
    if (CONFIG.enableTouch) setupTouch(carousel, slides, thumbnails, progressDots);
    if (CONFIG.pauseOnHover) setupHoverPause(carousel);

    // Update counter
    updateCounter(slides.length);

    // Start autoplay
    if (isAutoPlaying) {
      startAutoPlay(slides, thumbnails, progressDots);
    }

    console.log('%c🎨 Zorpido Featured Slider Activated!', 
      'color: #DC2626; font-size: 14px; font-weight: bold;');
  }

  /**
   * Setup navigation controls
   */
  function setupNavigation(slides, thumbnails, progressDots, prevBtn, nextBtn) {
    // Previous button
    prevBtn?.addEventListener('click', () => {
      if (isTransitioning) return;
      goToSlide(currentIndex - 1, slides, thumbnails, progressDots);
      resetAutoPlay(slides, thumbnails, progressDots);
    });

    // Next button
    nextBtn?.addEventListener('click', () => {
      if (isTransitioning) return;
      goToSlide(currentIndex + 1, slides, thumbnails, progressDots);
      resetAutoPlay(slides, thumbnails, progressDots);
    });

    // Thumbnail clicks
    thumbnails.forEach((thumb, index) => {
      thumb.addEventListener('click', () => {
        if (isTransitioning || index === currentIndex) return;
        goToSlide(index, slides, thumbnails, progressDots);
        resetAutoPlay(slides, thumbnails, progressDots);
      });
    });

    // Progress dot clicks
    progressDots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        if (isTransitioning || index === currentIndex) return;
        goToSlide(index, slides, thumbnails, progressDots);
        resetAutoPlay(slides, thumbnails, progressDots);
      });
    });
  }

  /**
   * Go to specific slide
   */
  function goToSlide(index, slides, thumbnails, progressDots) {
    if (isTransitioning) return;

    const newIndex = (index + slides.length) % slides.length;
    if (newIndex === currentIndex) return;

    isTransitioning = true;

    const currentSlide = slides[currentIndex];
    const nextSlide = slides[newIndex];

    // Animate transition
    currentSlide.classList.add('exit');
    nextSlide.classList.add('active');

    setTimeout(() => {
      currentSlide.classList.remove('active', 'exit');
      currentIndex = newIndex;
      updateUI(thumbnails, progressDots, slides.length);
      isTransitioning = false;
    }, CONFIG.transitionDuration);
  }

  /**
   * Update UI elements
   */
  function updateUI(thumbnails, progressDots, totalSlides) {
    // Update thumbnails
    thumbnails.forEach((thumb, index) => {
      thumb.classList.toggle('active', index === currentIndex);
    });

    // Update progress dots
    progressDots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentIndex);
    });

    // Update counter
    updateCounter(totalSlides);

    // Scroll active thumbnail into view (horizontal scroll only to avoid vertical jumps)
    const activeThumbnail = thumbnails[currentIndex];
    if (activeThumbnail) {
      try {
        const track = activeThumbnail.closest('.thumbnail-track');
        if (track) {
          // Calculate center offset and scroll the track horizontally
          const trackRect = track.getBoundingClientRect();
          const thumbRect = activeThumbnail.getBoundingClientRect();
          const trackCenter = trackRect.left + (trackRect.width / 2);
          const thumbCenter = thumbRect.left + (thumbRect.width / 2);
          const offset = thumbCenter - trackCenter;
          track.scrollBy({ left: offset, behavior: 'smooth' });
        } else {
          // Fallback: use scrollIntoView with nearest block to minimize vertical movement
          activeThumbnail.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }
      } catch (e) {
        // If anything goes wrong, fallback gracefully
        activeThumbnail.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    }
  }

  /**
   * Update slide counter
   */
  function updateCounter(total) {
    const currentEl = document.querySelector('.current-slide');
    const totalEl = document.querySelector('.total-slides');
    
    if (currentEl) currentEl.textContent = currentIndex + 1;
    if (totalEl) totalEl.textContent = total;
  }

  /**
   * Setup autoplay
   */
  function setupAutoplay(slides, thumbnails, progressDots, autoplayBtn) {
    if (!autoplayBtn) return;

    autoplayBtn.addEventListener('click', () => {
      isAutoPlaying = !isAutoPlaying;
      autoplayBtn.classList.toggle('active', isAutoPlaying);

      if (isAutoPlaying) {
        startAutoPlay(slides, thumbnails, progressDots);
      } else {
        stopAutoPlay();
      }
    });
  }

  /**
   * Start autoplay
   */
  function startAutoPlay(slides, thumbnails, progressDots) {
    if (slides.length <= 1) return;

    stopAutoPlay();
    autoPlayTimer = setInterval(() => {
      goToSlide(currentIndex + 1, slides, thumbnails, progressDots);
    }, CONFIG.autoPlayInterval);
  }

  /**
   * Stop autoplay
   */
  function stopAutoPlay() {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
  }

  /**
   * Reset autoplay
   */
  function resetAutoPlay(slides, thumbnails, progressDots) {
    if (isAutoPlaying) {
      startAutoPlay(slides, thumbnails, progressDots);
    }
  }

  /**
   * Setup hover pause
   */
  function setupHoverPause(carousel) {
    carousel.addEventListener('mouseenter', () => {
      stopAutoPlay();
    });

    carousel.addEventListener('mouseleave', () => {
      if (isAutoPlaying) {
        const slides = document.querySelectorAll('.carousel-slide');
        const thumbnails = document.querySelectorAll('.thumbnail-item');
        const progressDots = document.querySelectorAll('.progress-dot');
        startAutoPlay(slides, thumbnails, progressDots);
      }
    });
  }

  /**
   * Setup keyboard navigation
   */
  function setupKeyboard(slides, thumbnails, progressDots) {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        goToSlide(currentIndex - 1, slides, thumbnails, progressDots);
        resetAutoPlay(slides, thumbnails, progressDots);
      } else if (e.key === 'ArrowRight') {
        goToSlide(currentIndex + 1, slides, thumbnails, progressDots);
        resetAutoPlay(slides, thumbnails, progressDots);
      } else if (e.key === 'Escape') {
        closeFullscreen();
      }
    });
  }

  /**
   * Setup touch/swipe controls
   */
  function setupTouch(carousel, slides, thumbnails, progressDots) {
    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartY = 0;
    let touchEndY = 0;

    carousel.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe(slides, thumbnails, progressDots);
    }, { passive: true });

    function handleSwipe(slides, thumbnails, progressDots) {
      const swipeThreshold = 50;
      const diffX = touchStartX - touchEndX;
      const diffY = Math.abs(touchStartY - touchEndY);

      // Only register horizontal swipes
      if (diffY < swipeThreshold && Math.abs(diffX) > swipeThreshold) {
        if (diffX > 0) {
          // Swiped left - next
          goToSlide(currentIndex + 1, slides, thumbnails, progressDots);
        } else {
          // Swiped right - previous
          goToSlide(currentIndex - 1, slides, thumbnails, progressDots);
        }
        resetAutoPlay(slides, thumbnails, progressDots);
      }
    }
  }

  /**
   * Setup fullscreen functionality
   */
  function setupFullscreen(slides, images) {
    if (!CONFIG.enableFullscreen) return;

    const modal = document.getElementById('fullscreenModal');
    const modalImage = document.getElementById('fullscreenImage');
    const closeBtn = modal?.querySelector('.modal-close');
    const modalPrev = modal?.querySelector('.modal-prev');
    const modalNext = modal?.querySelector('.modal-next');

    if (!modal || !modalImage) return;

    // Click image to open fullscreen
    images.forEach((imageContainer, index) => {
      imageContainer.addEventListener('click', () => {
        const img = imageContainer.querySelector('.featured-image');
        if (img) {
          openFullscreen(img.src, img.alt);
        }
      });
    });

    // Close button
    closeBtn?.addEventListener('click', closeFullscreen);

    // Click outside to close
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeFullscreen();
      }
    });

    // Modal navigation
    modalPrev?.addEventListener('click', () => {
      navigateFullscreen(-1, slides);
    });

    modalNext?.addEventListener('click', () => {
      navigateFullscreen(1, slides);
    });

    function openFullscreen(src, alt) {
      modalImage.src = src;
      modalImage.alt = alt;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function navigateFullscreen(direction, slides) {
      const newIndex = (currentIndex + direction + slides.length) % slides.length;
      const newSlide = slides[newIndex];
      const newImage = newSlide.querySelector('.featured-image');
      
      if (newImage) {
        modalImage.style.opacity = '0';
        setTimeout(() => {
          modalImage.src = newImage.src;
          modalImage.alt = newImage.alt;
          modalImage.style.opacity = '1';
        }, 200);
      }
    }
  }

  /**
   * Close fullscreen modal
   */
  function closeFullscreen() {
    const modal = document.getElementById('fullscreenModal');
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  /**
   * Handle visibility change
   */
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopAutoPlay();
    } else if (isAutoPlaying) {
      const slides = document.querySelectorAll('.carousel-slide');
      const thumbnails = document.querySelectorAll('.thumbnail-item');
      const progressDots = document.querySelectorAll('.progress-dot');
      startAutoPlay(slides, thumbnails, progressDots);
    }
  });

  /**
   * Lazy load images
   */
  function lazyLoadImages() {
    const images = document.querySelectorAll('.featured-image[data-src]');
    
    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
            imageObserver.unobserve(img);
          }
        });
      });

      images.forEach(img => imageObserver.observe(img));
    } else {
      // Fallback for older browsers
      images.forEach(img => {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      });
    }
  }

  /**
   * Add entrance animations
   */
  function addEntranceAnimation() {
    const slider = document.querySelector('.zorpido-featured-slider');
    if (!slider) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          slider.style.opacity = '0';
          slider.style.transform = 'translateY(40px)';
          
          requestAnimationFrame(() => {
            slider.style.transition = 'all 0.8s ease-out';
            slider.style.opacity = '1';
            slider.style.transform = 'translateY(0)';
          });

          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    observer.observe(slider);
  }

  // Initialize additional features
  lazyLoadImages();
  addEntranceAnimation();

  /**
   * Public API
   */
  window.ZorpidoFeaturedSlider = {
    next: function() {
      const slides = document.querySelectorAll('.carousel-slide');
      const thumbnails = document.querySelectorAll('.thumbnail-item');
      const progressDots = document.querySelectorAll('.progress-dot');
      goToSlide(currentIndex + 1, slides, thumbnails, progressDots);
      resetAutoPlay(slides, thumbnails, progressDots);
    },
    prev: function() {
      const slides = document.querySelectorAll('.carousel-slide');
      const thumbnails = document.querySelectorAll('.thumbnail-item');
      const progressDots = document.querySelectorAll('.progress-dot');
      goToSlide(currentIndex - 1, slides, thumbnails, progressDots);
      resetAutoPlay(slides, thumbnails, progressDots);
    },
    goTo: function(index) {
      const slides = document.querySelectorAll('.carousel-slide');
      const thumbnails = document.querySelectorAll('.thumbnail-item');
      const progressDots = document.querySelectorAll('.progress-dot');
      goToSlide(index, slides, thumbnails, progressDots);
      resetAutoPlay(slides, thumbnails, progressDots);
    },
    pause: function() {
      isAutoPlaying = false;
      stopAutoPlay();
      const btn = document.querySelector('.autoplay-toggle');
      if (btn) btn.classList.remove('active');
    },
    play: function() {
      isAutoPlaying = true;
      const slides = document.querySelectorAll('.carousel-slide');
      const thumbnails = document.querySelectorAll('.thumbnail-item');
      const progressDots = document.querySelectorAll('.progress-dot');
      startAutoPlay(slides, thumbnails, progressDots);
      const btn = document.querySelector('.autoplay-toggle');
      if (btn) btn.classList.add('active');
    },
    getCurrentIndex: function() {
      return currentIndex;
    }
  };

})();





/**
 * ZORPIDO GALLERY SECTION - JavaScript
 * Enhanced Gallery with Modal Navigation
 */

(function() {
  'use strict';

  let currentImageIndex = 0;
  let totalImages = 0;
  let galleryImages = [];

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /**
   * Initialize gallery features
   */
  function init() {
    const gallerySection = document.querySelector('.zorpido-gallery-section');
    if (!gallerySection) return;

    // Initialize scroll animations
    initScrollAnimations();
    
    // Setup modal functionality
    setupModal();
    
    // Add hover effects
    addHoverEffects();
    
    // Setup keyboard navigation
    setupKeyboardNav();
    
    // Initialize lightbox features
    initLightbox();

    console.log('%c🖼️ Zorpido Gallery Activated!', 
      'color: #DC2626; font-size: 14px; font-weight: bold;');
  }

  /**
   * Initialize scroll animations
   */
  function initScrollAnimations() {
    // Check if AOS library is available
    if (typeof AOS !== 'undefined') {
      AOS.init({
        duration: 600,
        easing: 'ease-out-cubic',
        once: true,
        offset: 100
      });
    } else {
      // Fallback: Simple intersection observer
      const cards = document.querySelectorAll('.gallery-card');
      
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.style.opacity = '1';
              entry.target.style.transform = 'translateY(0)';
            }
          });
        }, {
          threshold: 0.1,
          rootMargin: '0px 0px -50px 0px'
        });

        cards.forEach((card, index) => {
          card.style.opacity = '0';
          card.style.transform = 'translateY(30px)';
          card.style.transition = `all 0.6s ease ${index * 0.05}s`;
          observer.observe(card);
        });
      }
    }
  }

  /**
   * Setup modal functionality
   */
  function setupModal() {
    const modal = document.getElementById('galleryModal');
    if (!modal) return;

  // Scope queries to the gallery section/modal to avoid picking up
  // similarly-named elements from other sliders (e.g. featured slider).
  const imageContainers = gallerySection.querySelectorAll('.image-container');
  const modalImage = document.getElementById('galleryModalImage');
  const modalTitle = document.getElementById('galleryModalTitle');
  const currentImageEl = document.getElementById('currentImage');
  const totalImagesEl = document.getElementById('totalImages');
  const prevBtn = document.getElementById('modalPrev');
  const nextBtn = document.getElementById('modalNext');
  // Thumbnails inside the modal's thumbnail nav (scope to modal)
  const thumbnails = modal.querySelectorAll('.thumbnail-item');

    // Collect all image data (include server id when available)
    galleryImages = Array.from(imageContainers).map(container => ({
      url: container.dataset.image,
      title: container.dataset.title || 'Untitled',
      id: container.dataset.id ? parseInt(container.dataset.id) : null,
      index: parseInt(container.dataset.index)
    }));

    totalImages = galleryImages.length;
    if (totalImagesEl) totalImagesEl.textContent = totalImages;

    // Open modal on image click
    imageContainers.forEach((container) => {
      container.addEventListener('click', function() {
        currentImageIndex = parseInt(this.dataset.index);
        updateModalImage();
      });
    });

    // Navigation buttons
    if (prevBtn) {
      prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navigateImage(-1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        navigateImage(1);
      });
    }

    // Thumbnail navigation
    thumbnails.forEach((thumb) => {
      thumb.addEventListener('click', function() {
        currentImageIndex = parseInt(this.dataset.index);
        updateModalImage();
      });
    });

    // Action buttons
    setupActionButtons();

    // Swipe support for mobile
    setupTouchNavigation(modal);
  }

  /**
   * Update modal image
   */
  function updateModalImage() {
    const modalImage = document.getElementById('galleryModalImage');
    const modalTitle = document.getElementById('galleryModalTitle');
    const currentImageEl = document.getElementById('currentImage');
    const loader = document.querySelector('.image-loader');
    const thumbnails = document.querySelectorAll('.thumbnail-item');

    if (!galleryImages[currentImageIndex]) return;

    const imageData = galleryImages[currentImageIndex];

    // Show loader and hide current image
    if (loader) loader.style.display = 'block';
    if (modalImage) {
      modalImage.style.opacity = '0';
      modalImage.style.display = 'none';
    }

    // Preload new image
    const img = new Image();
    img.onload = function() {
      if (modalImage) {
        modalImage.src = imageData.url;
        modalImage.alt = imageData.title;
        modalImage.style.display = 'block';
        
        // Force reflow
        void modalImage.offsetWidth;
        
        // Fade in
        setTimeout(() => {
          modalImage.style.opacity = '1';
        }, 50);
      }
      if (loader) loader.style.display = 'none';
    };
    
    img.onerror = function() {
      if (loader) loader.style.display = 'none';
      showNotification('Failed to load image', 'error');
    };
    
    img.src = imageData.url;

    // Update title and counter
    if (modalTitle) modalTitle.textContent = imageData.title;
    if (currentImageEl) currentImageEl.textContent = currentImageIndex + 1;

    // Update active thumbnail
    thumbnails.forEach((thumb, index) => {
      thumb.classList.toggle('active', index === currentImageIndex);
    });

    // Scroll thumbnail into view
    if (thumbnails[currentImageIndex]) {
      thumbnails[currentImageIndex].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center'
      });
    }
  }

  /**
   * Navigate to next/previous image
   */
  function navigateImage(direction) {
    currentImageIndex = (currentImageIndex + direction + totalImages) % totalImages;
    updateModalImage();
  }

  /**
   * Setup action buttons
   */
  function setupActionButtons() {
    const downloadBtn = document.getElementById('downloadBtn');
    const shareBtn = document.getElementById('shareBtn');
    const shareMenu = document.getElementById('shareMenu');
    const closeShareMenu = document.getElementById('closeShareMenu');
    const shareOptions = document.querySelectorAll('.share-option');

    // Download button - Direct download to device
    if (downloadBtn) {
      downloadBtn.addEventListener('click', async () => {
        const imageData = galleryImages[currentImageIndex];
        if (!imageData) return;

        // If we have a server-side id for the image, use the download endpoint (simpler and preserves original file)
        if (imageData.id) {
          // use absolute path to trigger file download
          window.location.href = `/gallery/download/${imageData.id}/`;
          return;
        }

        // Fallback: fetch blob and download client-side
        try {
          // Show loading state
          downloadBtn.disabled = true;
          downloadBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Downloading...';

          // Fetch the image as blob
          const response = await fetch(imageData.url);
          const blob = await response.blob();
          
          // Create download link
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          
          // Generate filename
          const filename = `zorpido-${imageData.title.replace(/[^a-z0-9]/gi, '-').toLowerCase()}-${Date.now()}.jpg`;
          a.download = filename;
          
          // Trigger download
          document.body.appendChild(a);
          a.click();
          
          // Cleanup
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
          }, 100);

          // Reset button
          downloadBtn.disabled = false;
          downloadBtn.innerHTML = '<i class="bi bi-download"></i> Download';
          
          showNotification('Image downloaded successfully! Check your downloads folder.', 'success');
        } catch (error) {
          console.error('Download failed:', error);
          downloadBtn.disabled = false;
          downloadBtn.innerHTML = '<i class="bi bi-download"></i> Download';
          showNotification('Failed to download image. Please try again.', 'error');
        }
      });
    }

    // Share button - Show share menu
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        if (shareMenu) {
          shareMenu.classList.add('active');
        }
      });
    }

    // Close share menu
    if (closeShareMenu) {
      closeShareMenu.addEventListener('click', () => {
        if (shareMenu) {
          shareMenu.classList.remove('active');
        }
      });
    }

    // Share options
    shareOptions.forEach(option => {
      option.addEventListener('click', async () => {
        const platform = option.dataset.platform;
        const imageData = galleryImages[currentImageIndex];
        if (!imageData) return;

        const imageUrl = imageData.url;
        const shareText = `Check out this photo from Zorpido: ${imageData.title}`;

        try {
          // Use Web Share API on supported devices (mobile) for a native share sheet
          if (navigator.share) {
            try {
              await navigator.share({
                title: imageData.title,
                text: shareText,
                url: imageUrl
              });
              showNotification('Shared successfully', 'success');
            } catch (err) {
              // User may have cancelled; silently ignore
            }

            // close menu
            if (shareMenu) shareMenu.classList.remove('active');
            return;
          }

          // Desktop / fallback: open social share links using the image URL
          switch(platform) {
            case 'whatsapp':
              // WhatsApp sharing
              const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(shareText + ' ' + imageUrl)}`;
              window.open(whatsappUrl, '_blank');
              showNotification('Opening WhatsApp...', 'success');
              break;

            case 'facebook':
              // Facebook sharing (shares a URL; sharing an image URL is acceptable)
              const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(imageUrl)}&quote=${encodeURIComponent(shareText)}`;
              window.open(facebookUrl, '_blank', 'width=600,height=400');
              showNotification('Opening Facebook...', 'success');
              break;

            case 'messenger':
              // Messenger fallback - open Facebook share dialog for link sharing
              const messengerUrl = `https://www.facebook.com/dialog/send?link=${encodeURIComponent(imageUrl)}&app_id=145634995501895&redirect_uri=${encodeURIComponent(window.location.href)}`;
              window.open(messengerUrl, '_blank', 'width=600,height=600');
              showNotification('Opening Messenger...', 'success');
              break;

            case 'instagram':
              // Instagram - cannot share via URL; copy link and prompt
              await navigator.clipboard.writeText(imageUrl);
              showNotification('Image link copied! Open Instagram and paste in your story or post.', 'info');
              setTimeout(() => {
                window.open('https://www.instagram.com/', '_blank');
              }, 1200);
              break;

            case 'twitter':
              // Twitter sharing
              const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(imageUrl)}`;
              window.open(twitterUrl, '_blank', 'width=600,height=400');
              showNotification('Opening Twitter...', 'success');
              break;

            case 'copy':
              // Copy link to clipboard
              await navigator.clipboard.writeText(imageUrl);
              showNotification('Link copied to clipboard!', 'success');
              break;

            default:
              showNotification('Share option not available', 'error');
          }

          // Close share menu after selection
          if (shareMenu) {
            setTimeout(() => {
              shareMenu.classList.remove('active');
            }, 500);
          }
        } catch (error) {
          console.error('Share failed:', error);
          showNotification('Failed to share. Please try again.', 'error');
        }
      });
    });

    // Close share menu when clicking outside
    document.addEventListener('click', (e) => {
      if (shareMenu && shareMenu.classList.contains('active')) {
        if (!shareMenu.contains(e.target) && !shareBtn.contains(e.target)) {
          shareMenu.classList.remove('active');
        }
      }
    });
  }

  /**
   * Setup keyboard navigation
   */
  function setupKeyboardNav() {
    const modal = document.getElementById('galleryModal');
    if (!modal) return;

    document.addEventListener('keydown', (e) => {
      // Only handle keys when modal is open
      if (!modal.classList.contains('show')) return;

      switch(e.key) {
        case 'ArrowLeft':
          navigateImage(-1);
          break;
        case 'ArrowRight':
          navigateImage(1);
          break;
        case 'Escape':
          // Bootstrap will handle closing
          break;
      }
    });
  }

  /**
   * Setup touch navigation for swipe
   */
  function setupTouchNavigation(modal) {
    let touchStartX = 0;
    let touchEndX = 0;
    let touchStartY = 0;
    let touchEndY = 0;

    const imageViewer = modal.querySelector('.image-viewer');
    if (!imageViewer) return;

    imageViewer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    imageViewer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const swipeThreshold = 50;
      const diffX = touchStartX - touchEndX;
      const diffY = Math.abs(touchStartY - touchEndY);

      // Only horizontal swipes
      if (diffY < swipeThreshold && Math.abs(diffX) > swipeThreshold) {
        if (diffX > 0) {
          // Swipe left - next
          navigateImage(1);
        } else {
          // Swipe right - previous
          navigateImage(-1);
        }
      }
    }
  }

  /**
   * Add hover effects to cards
   */
  function addHoverEffects() {
    const cards = document.querySelectorAll('.gallery-card');

    cards.forEach(card => {
      const imageContainer = card.querySelector('.image-container');
      
      imageContainer.addEventListener('mousemove', (e) => {
        const rect = imageContainer.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        imageContainer.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
      });
      
      imageContainer.addEventListener('mouseleave', () => {
        imageContainer.style.transform = '';
      });
    });
  }

  /**
   * Initialize lightbox features
   */
  function initLightbox() {
    const modal = document.getElementById('galleryModal');
    if (!modal) return;

    // Zoom on image click
    const modalImage = document.getElementById('galleryModalImage');
    if (modalImage) {
      let isZoomed = false;
      
      modalImage.addEventListener('click', () => {
        isZoomed = !isZoomed;
        modalImage.style.transform = isZoomed ? 'scale(1.5)' : 'scale(1)';
        modalImage.style.cursor = isZoomed ? 'zoom-out' : 'zoom-in';
        modalImage.style.transition = 'transform 0.3s ease';
      });
    }
  }

  /**
   * Show notification
   */
  function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `gallery-notification notification-${type}`;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 1rem 1.5rem;
      background: ${type === 'success' ? '#10B981' : type === 'error' ? '#DC2626' : '#3B82F6'};
      color: white;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      z-index: 10000;
      animation: slideIn 0.3s ease;
      font-weight: 600;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);

    // Add animations if not exist
    if (!document.querySelector('style[data-notification-anim]')) {
      const style = document.createElement('style');
      style.setAttribute('data-notification-anim', 'true');
      style.textContent = `
        @keyframes slideIn {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes slideOut {
          from {
            transform: translateX(0);
            opacity: 1;
          }
          to {
            transform: translateX(400px);
            opacity: 0;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  /**
   * Public API
   */
  window.ZorpidoGallery = {
    openImage: function(index) {
      currentImageIndex = index;
      const modal = new bootstrap.Modal(document.getElementById('galleryModal'));
      modal.show();
      updateModalImage();
    },
    nextImage: function() {
      navigateImage(1);
    },
    prevImage: function() {
      navigateImage(-1);
    },
    getCurrentIndex: function() {
      return currentImageIndex;
    }
  };

})();





/* ===============================================
   TESTIMONIALS SECTION - JAVASCRIPT
   Auto-sliding, Manual Controls, Smooth Animations
   =============================================== */

(function () {
  'use strict';

  // Wait for DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', function () {

    // Get all necessary elements
    const slider = document.querySelector('.testimonial-slider');
    const cards = document.querySelectorAll('.testimonial-card');
    const dots = document.querySelectorAll('.slider-dots .dot');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const progressFill = document.querySelector('.progress-fill');

    // Check if testimonials exist
    if (!slider || cards.length === 0) {
      return;
    }

    // Configuration
    let currentIndex = 0;
    let autoSlideInterval;
    const autoSlideDelay = 5000; // 5 seconds per slide
    let isTransitioning = false;

    /* -----------------
       Initialize Slider
       ----------------- */
    function init() {
      // Set first card as active
      showSlide(0);

      // Start auto-sliding
      startAutoSlide();

      // Add event listeners
      attachEventListeners();
    }

    /* -----------------
       Show Specific Slide
       ----------------- */
    function showSlide(index, direction = 'next') {
      // Prevent rapid clicking
      if (isTransitioning) return;
      isTransitioning = true;

      // Remove all active classes
      cards.forEach(card => {
        card.classList.remove('active', 'prev');
      });

      dots.forEach(dot => {
        dot.classList.remove('active');
      });

      // Add prev class to current card for exit animation
      if (direction === 'prev') {
        cards[currentIndex].classList.add('prev');
      }

      // Update index
      currentIndex = index;

      // Ensure index is within bounds
      if (currentIndex >= cards.length) {
        currentIndex = 0;
      } else if (currentIndex < 0) {
        currentIndex = cards.length - 1;
      }

      // Add active class to new card
      setTimeout(() => {
        cards[currentIndex].classList.add('active');
        dots[currentIndex].classList.add('active');
        isTransitioning = false;
      }, 50);

      // Reset progress bar
      resetProgress();
    }

    /* -----------------
       Next Slide
       ----------------- */
    function nextSlide() {
      const nextIndex = (currentIndex + 1) % cards.length;
      showSlide(nextIndex, 'next');
    }

    /* -----------------
       Previous Slide
       ----------------- */
    function prevSlide() {
      const prevIndex = (currentIndex - 1 + cards.length) % cards.length;
      showSlide(prevIndex, 'prev');
    }

    /* -----------------
       Go to Specific Slide
       ----------------- */
    function goToSlide(index) {
      if (index === currentIndex) return;

      const direction = index > currentIndex ? 'next' : 'prev';
      showSlide(index, direction);
    }

    /* -----------------
       Auto-Slide Functions
       ----------------- */
    function startAutoSlide() {
      autoSlideInterval = setInterval(() => {
        nextSlide();
      }, autoSlideDelay);
    }

    function stopAutoSlide() {
      clearInterval(autoSlideInterval);
    }

    function resetAutoSlide() {
      stopAutoSlide();
      startAutoSlide();
    }

    /* -----------------
       Progress Bar Animation
       ----------------- */
    function resetProgress() {
      if (!progressFill) return;

      // Reset animation
      progressFill.style.animation = 'none';
      progressFill.offsetHeight; // Trigger reflow
      progressFill.style.animation = null;
    }

    /* -----------------
       Event Listeners
       ----------------- */
    function attachEventListeners() {

      // Previous button
      if (prevBtn) {
        prevBtn.addEventListener('click', function () {
          prevSlide();
          resetAutoSlide();
        });
      }

      // Next button
      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          nextSlide();
          resetAutoSlide();
        });
      }

      // Dot navigation
      dots.forEach((dot, index) => {
        dot.addEventListener('click', function () {
          goToSlide(index);
          resetAutoSlide();
        });
      });

      // Keyboard navigation
      document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
          prevSlide();
          resetAutoSlide();
        } else if (e.key === 'ArrowRight') {
          nextSlide();
          resetAutoSlide();
        }
      });

      // Pause on hover
      if (slider) {
        slider.addEventListener('mouseenter', function () {
          stopAutoSlide();
        });

        slider.addEventListener('mouseleave', function () {
          startAutoSlide();
        });
      }

      // Touch/Swipe support for mobile
      let touchStartX = 0;
      let touchEndX = 0;

      if (slider) {
        slider.addEventListener('touchstart', function (e) {
          touchStartX = e.changedTouches[0].screenX;
          stopAutoSlide();
        }, { passive: true });

        slider.addEventListener('touchend', function (e) {
          touchEndX = e.changedTouches[0].screenX;
          handleSwipe();
          startAutoSlide();
        }, { passive: true });
      }

      function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
          if (diff > 0) {
            // Swipe left - next slide
            nextSlide();
          } else {
            // Swipe right - previous slide
            prevSlide();
          }
        }
      }

      // Pause auto-slide when page is not visible
      document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
          stopAutoSlide();
        } else {
          startAutoSlide();
        }
      });
    }

    /* -----------------
       Add Ripple Effect to Buttons
       ----------------- */
    function createRipple(event) {
      const button = event.currentTarget;
      const ripple = document.createElement('span');
      const diameter = Math.max(button.clientWidth, button.clientHeight);
      const radius = diameter / 2;

      ripple.style.width = ripple.style.height = `${diameter}px`;
      ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
      ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
      ripple.classList.add('ripple');

      const existingRipple = button.querySelector('.ripple');
      if (existingRipple) {
        existingRipple.remove();
      }

      button.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 600);
    }

    // Add ripple effect to navigation buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(button => {
      button.addEventListener('click', createRipple);
    });

    /* -----------------
       Smooth Scroll for Share Button
       ----------------- */
    const shareBtn = document.querySelector('.btn-share');
    if (shareBtn) {
      shareBtn.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          const targetId = href.substring(1);
          const targetElement = document.getElementById(targetId);

          if (targetElement) {
            targetElement.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        }
      });
    }

    /* -----------------
       Initialize
       ----------------- */
    init();

    // Accessibility: Announce slide changes to screen readers
    function announceSlideChange() {
      const announcement = document.createElement('div');
      announcement.setAttribute('role', 'status');
      announcement.setAttribute('aria-live', 'polite');
      announcement.setAttribute('aria-atomic', 'true');
      announcement.className = 'sr-only';
      announcement.style.position = 'absolute';
      announcement.style.left = '-10000px';
      announcement.style.width = '1px';
      announcement.style.height = '1px';
      announcement.style.overflow = 'hidden';

      const currentCard = cards[currentIndex];
      const customerName = currentCard.querySelector('.customer-name');

      if (customerName) {
        announcement.textContent = `Showing testimonial ${currentIndex + 1} of ${cards.length} from ${customerName.textContent}`;
      }

      document.body.appendChild(announcement);

      setTimeout(() => {
        announcement.remove();
      }, 1000);
    }

    // Update showSlide to include accessibility announcement
    const originalShowSlide = showSlide;
    showSlide = function (index, direction) {
      originalShowSlide(index, direction);
      announceSlideChange();
    };

  });

})();

/* -----------------
   Additional CSS for Ripple Effect
   Add this to your CSS if not already present
   ----------------- */
/*
.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  transform: scale(0);
  animation: ripple-animation 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
*/
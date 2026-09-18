/**
 * ATELIER & CO. - Modern Luxury E-Commerce Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  initStickyHeader();
  initCartDrawer();
  initQuickView();
  initWishlist();
  initVariantPickers();
  initImageGalleries();
});

// ---------------------------------------------------------
// Toast System
// ---------------------------------------------------------
function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = '✦';
  if (type === 'success') icon = '✓';
  if (type === 'danger' || type === 'error') icon = '✕';
  if (type === 'warning') icon = '⚠';

  toast.innerHTML = `
    <span style="font-weight: 700; color: var(--gold-light);">${icon}</span>
    <span style="flex: 1; font-size: 0.9rem;">${message}</span>
    <button style="background:transparent; color:var(--text-muted); cursor:pointer; font-size:1.1rem;" onclick="this.parentElement.remove()">×</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ---------------------------------------------------------
// Sticky Header
// ---------------------------------------------------------
function initStickyHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

// ---------------------------------------------------------
// Cart Drawer & AJAX Cart Operations
// ---------------------------------------------------------
function initCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const backdrop = document.getElementById('drawerBackdrop');
  const openButtons = document.querySelectorAll('[data-open-cart]');
  const closeButton = document.getElementById('closeCartDrawer');

  function openDrawer() {
    if (!drawer || !backdrop) return;
    refreshCartDrawer();
    drawer.classList.add('active');
    backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    if (!drawer || !backdrop) return;
    drawer.classList.remove('active');
    backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  openButtons.forEach(btn => btn.addEventListener('click', (e) => {
    e.preventDefault();
    openDrawer();
  }));

  if (closeButton) closeButton.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('active')) {
      closeDrawer();
    }
  });

  window.openCartDrawer = openDrawer;
  window.closeCartDrawer = closeDrawer;
}

function updateGlobalBadge(count) {
  const badges = document.querySelectorAll('.cart-badge-count');
  badges.forEach(b => {
    b.textContent = count;
    b.style.display = count > 0 ? 'flex' : 'none';
  });
}

async function refreshCartDrawer() {
  const body = document.getElementById('cartDrawerBody');
  const subtotalEl = document.getElementById('cartDrawerSubtotal');
  const shippingMsgEl = document.getElementById('cartDrawerShippingMsg');
  const progressFill = document.getElementById('cartDrawerProgressFill');
  
  if (!body) return;

  try {
    const res = await fetch('/api/cart/drawer');
    const data = await res.json();

    updateGlobalBadge(data.total_quantity);

    if (!data.items || data.items.length === 0) {
      body.innerHTML = `
        <div style="text-align: center; padding: 4rem 1rem;">
          <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.4;">🛍</div>
          <h4 style="font-size: 1.25rem; margin-bottom: 0.5rem;">Your Shopping Bag is Empty</h4>
          <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.5rem;">Discover our latest haute couture arrivals.</p>
          <a href="/products" class="btn btn-primary btn-sm" onclick="window.closeCartDrawer()">Explore Catalog</a>
        </div>
      `;
      if (subtotalEl) subtotalEl.textContent = '₹0.00';
      return;
    }

    let html = '';
    data.items.forEach(it => {
      html += `
        <div class="cart-item-card" data-item-id="${it.cart_item_id}">
          <div class="cart-item-img">
            <img src="${it.image_url}" alt="${it.product_name}" loading="lazy">
          </div>
          <div class="cart-item-details">
            <h5 style="font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem;">${it.product_name}</h5>
            <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.5rem;">
              Size: <span style="color:var(--gold-light);">${it.size}</span> | Color: <span style="color:var(--text-secondary);">${it.color}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: auto;">
              <div class="quantity-control" style="transform: scale(0.85); transform-origin: left center;">
                <button class="qty-btn" onclick="updateCartItemQty(${it.cart_item_id}, ${it.quantity - 1})">-</button>
                <span class="qty-input" style="display:inline-flex; align-items:center; justify-content:center;">${it.quantity}</span>
                <button class="qty-btn" onclick="updateCartItemQty(${it.cart_item_id}, ${it.quantity + 1})">+</button>
              </div>
              <div style="text-align: right;">
                <div style="font-size: 0.95rem; font-weight: 700; color: var(--gold-light);">₹${it.subtotal.toFixed(2)}</div>
                <button onclick="updateCartItemQty(${it.cart_item_id}, 0)" style="background:transparent; color:var(--accent-rose); font-size:0.75rem; cursor:pointer; text-decoration:underline;">Remove</button>
              </div>
            </div>
          </div>
        </div>
      `;
    });

    body.innerHTML = html;
    if (subtotalEl) subtotalEl.textContent = `₹${data.subtotal.toFixed(2)}`;

    if (shippingMsgEl && progressFill) {
      progressFill.style.width = `${data.free_shipping_progress}%`;
      if (data.free_shipping_remaining <= 0) {
        shippingMsgEl.innerHTML = `🎉 <strong>Congratulations!</strong> You unlocked Free Express Shipping!`;
      } else {
        shippingMsgEl.innerHTML = `Add <strong>₹${data.free_shipping_remaining.toFixed(2)}</strong> more to get <strong>FREE SHIPPING</strong>`;
      }
    }

  } catch (err) {
    console.error('Error fetching cart drawer:', err);
  }
}

async function updateCartItemQty(itemId, newQty) {
  try {
    const res = await fetch('/api/cart/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cart_item_id: itemId, quantity: newQty })
    });
    const data = await res.json();
    if (data.success) {
      refreshCartDrawer();
      const cartPageRow = document.querySelector(`[data-cart-page-item="${itemId}"]`);
      if (cartPageRow) {
        window.location.reload();
      }
    }
  } catch (err) {
    console.error('Error updating cart:', err);
  }
}

async function addToCartAjax(variantId, quantity = 1) {
  try {
    const res = await fetch('/api/cart/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ variant_id: variantId, quantity: quantity })
    });
    const data = await res.json();

    if (data.success) {
      showToast(data.message, 'success');
      updateGlobalBadge(data.cart_count);
      if (window.openCartDrawer) window.openCartDrawer();
    } else {
      showToast(data.message || 'Unable to add item', 'warning');
    }
  } catch (err) {
    showToast('Failed to connect. Please try again.', 'danger');
  }
}

// ---------------------------------------------------------
// Wishlist Toggle
// ---------------------------------------------------------
function initWishlist() {
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-wishlist-toggle]');
    if (!btn) return;
    e.preventDefault();

    const productId = btn.getAttribute('data-wishlist-toggle');
    try {
      const res = await fetch('/api/wishlist/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
      });
      const data = await res.json();

      if (data.require_login) {
        showToast(data.message, 'warning');
        setTimeout(() => window.location.href = '/login', 1000);
        return;
      }

      if (data.success) {
        if (data.added) {
          btn.classList.add('active');
          btn.innerHTML = '♥';
          showToast(data.message, 'success');
        } else {
          btn.classList.remove('active');
          btn.innerHTML = '♡';
          showToast(data.message, 'info');
        }

        const countBadges = document.querySelectorAll('.wishlist-badge-count');
        countBadges.forEach(b => {
          b.textContent = data.wishlist_count;
          b.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
        });
      }
    } catch (err) {
      console.error(err);
    }
  });
}

// ---------------------------------------------------------
// Quick View Modal
// ---------------------------------------------------------
function initQuickView() {
  const modal = document.getElementById('quickViewModal');
  const backdrop = document.getElementById('modalBackdrop');
  if (!modal) return;

  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-quickview-id]');
    if (!btn) return;
    e.preventDefault();

    const pid = btn.getAttribute('data-quickview-id');
    try {
      const res = await fetch(`/api/product/${pid}/quickview`);
      const prod = await res.json();

      document.getElementById('qvImage').src = prod.image_url;
      document.getElementById('qvTitle').textContent = prod.product_name;
      document.getElementById('qvSubtitle').textContent = prod.subtitle || '';
      document.getElementById('qvPrice').textContent = `₹${prod.base_price.toFixed(2)}`;
      document.getElementById('qvDescription').textContent = prod.description;
      document.getElementById('qvRating').textContent = `${prod.rating} (${prod.reviews_count} reviews)`;
      
      const linkEl = document.getElementById('qvViewFullLink');
      if (linkEl) linkEl.href = `/product/${prod.product_id}`;

      const variantContainer = document.getElementById('qvVariants');
      if (variantContainer) {
        let varHtml = '<div style="margin-bottom: 1rem;"><div style="font-size:0.85rem; font-weight:600; margin-bottom:0.5rem;">Select Variant:</div><div style="display:flex; flex-wrap:wrap; gap:0.5rem;">';
        prod.variants.forEach((v, idx) => {
          varHtml += `
            <button type="button" class="size-chip ${idx === 0 ? 'selected' : ''}" 
              data-qv-variant-id="${v.variant_id}" 
              data-qv-price="${v.price}"
              onclick="selectQvVariant(this)">
              ${v.size} - ${v.color}
            </button>
          `;
        });
        varHtml += '</div></div>';
        variantContainer.innerHTML = varHtml;
      }

      const qvAddBtn = document.getElementById('qvAddToCartBtn');
      if (qvAddBtn && prod.variants.length > 0) {
        qvAddBtn.onclick = () => {
          const selected = document.querySelector('[data-qv-variant-id].selected');
          const varId = selected ? selected.getAttribute('data-qv-variant-id') : prod.variants[0].variant_id;
          addToCartAjax(varId, 1);
          closeModal();
        };
      }

      openModal();
    } catch (err) {
      console.error('Quickview error:', err);
    }
  });

  function openModal() {
    modal.classList.add('active');
    backdrop.classList.add('active');
  }

  function closeModal() {
    modal.classList.remove('active');
    backdrop.classList.remove('active');
  }

  const closeBtn = document.getElementById('closeQuickView');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (backdrop) backdrop.addEventListener('click', closeModal);
}

window.selectQvVariant = function(btn) {
  document.querySelectorAll('[data-qv-variant-id]').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  const price = btn.getAttribute('data-qv-price');
  if (price) {
    document.getElementById('qvPrice').textContent = `₹${parseFloat(price).toFixed(2)}`;
  }
};

// ---------------------------------------------------------
// Image Gallery & Thumbnails on Detail Page
// ---------------------------------------------------------
function initImageGalleries() {
  const mainImage = document.getElementById('mainProductDisplay');
  const thumbs = document.querySelectorAll('.thumb-item');

  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        const newSrc = thumb.getAttribute('data-img-src');
        if (newSrc) {
          mainImage.style.opacity = '0.5';
          mainImage.src = newSrc;
          setTimeout(() => mainImage.style.opacity = '1', 150);
        }
      });
    });
  }
}

// ---------------------------------------------------------
// Variant Selection on Product Detail Page
// ---------------------------------------------------------
function initVariantPickers() {
  const sizeChips = document.querySelectorAll('.size-chip[data-size]');
  const colorDots = document.querySelectorAll('.color-dot[data-color]');
  const variantInput = document.getElementById('selectedVariantId');
  const priceDisplay = document.getElementById('detailProductPrice');
  const stockIndicator = document.getElementById('variantStockIndicator');

  function updateSelectedVariant() {
    const activeSize = document.querySelector('.size-chip.selected')?.getAttribute('data-size');
    const activeColor = document.querySelector('.color-dot.selected')?.getAttribute('data-color');

    const variantsDataEl = document.getElementById('productVariantsJson');
    if (!variantsDataEl || !variantInput) return;

    try {
      const variants = JSON.parse(variantsDataEl.textContent);
      const match = variants.find(v => 
        (!activeSize || v.size_label === activeSize) && 
        (!activeColor || v.color === activeColor)
      ) || variants[0];

      if (match) {
        variantInput.value = match.variant_id;
        if (priceDisplay) priceDisplay.textContent = `₹${match.price.toFixed(2)}`;
        if (stockIndicator) {
          if (match.stock_quantity > 0) {
            stockIndicator.innerHTML = `<span style="color:var(--accent-emerald);">● In Stock (${match.stock_quantity} available)</span>`;
          } else {
            stockIndicator.innerHTML = `<span style="color:var(--accent-rose);">● Out of Stock</span>`;
          }
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  sizeChips.forEach(chip => {
    chip.addEventListener('click', () => {
      sizeChips.forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');
      updateSelectedVariant();
    });
  });

  colorDots.forEach(dot => {
    dot.addEventListener('click', () => {
      colorDots.forEach(d => d.classList.remove('selected'));
      dot.classList.add('selected');
      updateSelectedVariant();
    });
  });
}

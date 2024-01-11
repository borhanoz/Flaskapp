
  // Select the Add to Cart buttons and the cart count badge
  const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
  const cartCountBadge = document.getElementById('cart-count-badge');

  // Function to update the cart count
  function updateCartCount() {
    fetch('/get_cart_count')
      .then(response => response.json())
      .then(data => {
        console.log(data.count);
        cartCountBadge.textContent = data.count;
        cartCountBadge.classList.remove('d-none'); // Show the badge
      });
  }

  // Attach event listeners to the buttons
  addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Prevent form submission
      event.preventDefault();

      // Send AJAX request to add product to cart
      const productId = button.dataset.productId;
      fetch(`/add_to_cart/${productId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Update cart count and display success message
            updateCartCount();
            alert('Product added to cart successfully!');
          } else {
            alert('Error adding product to cart');
          }
        });
    });
  });


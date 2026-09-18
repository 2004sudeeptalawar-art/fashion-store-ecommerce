// main.js

// Function to add a variant to cart via AJAX
function addToCart(variantId, quantity) {
  fetch("/add_to_cart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ variant_id: variantId, quantity: quantity }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Added to cart!");
      }
    })
    .catch((err) => console.error("Error adding to cart:", err));
}

// Function to remove an item from the cart via AJAX
function removeFromCart(itemId) {
  fetch("/remove_from_cart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ item_id: itemId }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Removed from cart!");
        // Optionally, refresh the cart display
        location.reload();
      }
    })
    .catch((err) => console.error("Error removing from cart:", err));
}

// Function to update the quantity of an item in the cart via AJAX
function updateCartItem(itemId, quantity) {
  fetch("/update_cart_item", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ item_id: itemId, quantity: quantity }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
      } else {
        alert("Cart updated!");
        // Optionally, refresh the cart display
        location.reload();
      }
    })
    .catch((err) => console.error("Error updating cart item:", err));
}
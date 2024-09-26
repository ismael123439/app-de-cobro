// Función para añadir un producto al carrito
const addToCartButtons = document.querySelectorAll('.add-to-cart');
addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const product = button.parentElement;
        const productName = product.getAttribute('data-name');
        const productPrice = product.getAttribute('data-price');

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart.push({ name: productName, price: productPrice });
        localStorage.setItem('cart', JSON.stringify(cart));

        alert(`${productName} añadido al carrito.`);
    });
});

// Función para mostrar el contenido del carrito
if (window.location.pathname.includes('/templates/carrito.html')) {
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    const cartList = document.getElementById('cart-items');
    const totalPriceEl = document.getElementById('total-price');
    let totalPrice = 0;

    cartItems.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price}`;
        cartList.appendChild(li);
        totalPrice += parseInt(item.price);
    });

    totalPriceEl.textContent = `Precio total: $${totalPrice}`;
}

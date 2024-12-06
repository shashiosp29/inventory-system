const API_URL = 'http://localhost:5000';

async function loadItems() {
    try {
        const response = await fetch(`${API_URL}/items`);
        const items = await response.json();
        const inventoryList = document.getElementById('inventoryList');
        inventoryList.innerHTML = '';

        items.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>
                    <button onclick="removeItem(${item.id})">Remove</button>
                </td>
            `;
            inventoryList.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading items:', error);
    }
}

async function addItem() {
    const nameInput = document.getElementById('itemName');
    const quantityInput = document.getElementById('itemQuantity');

    if (!nameInput.value || !quantityInput.value) {
        alert('Please fill in both name and quantity');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: nameInput.value,
                quantity: parseInt(quantityInput.value)
            })
        });

        if (response.ok) {
            nameInput.value = '';
            quantityInput.value = '';
            loadItems();
        }
    } catch (error) {
        console.error('Error adding item:', error);
    }
}

async function removeItem(itemId) {
    try {
        const response = await fetch(`${API_URL}/items/${itemId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadItems();
        }
    } catch (error) {
        console.error('Error removing item:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadItems);
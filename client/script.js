function fetchItems() {
    fetch('/api/items')
        .then(response => response.json())
        .then(data => {
            const itemList = document.getElementById('itemList');
            itemList.innerHTML = ''; 
            data.forEach(item => { 
                const listItem = document.createElement('li');
                listItem.textContent = `${item[1]} - Quantity: ${item[2]}` + "  "; 

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => deleteItem(item[0]); 

                listItem.appendChild(deleteButton);
                itemList.appendChild(listItem);

            });

        })
        .catch(error => console.error("Error fetching items:", error));

}

function addItem() {
    const itemName = document.getElementById('itemName').value;
    const itemQuantity = parseInt(document.getElementById('itemQuantity').value, 10);


    fetch('/api/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: itemName, quantity: itemQuantity })
    })
        .then(() => {
            fetchItems();
            document.getElementById('itemName').value = '';
            document.getElementById('itemQuantity').value = 0;
        })
        .catch(error => console.error("Error adding item:", error));
}

function deleteItem(itemId) {
    fetch(`/api/items/${itemId}`, {
        method: 'DELETE'
    })
        .then(() => fetchItems())
        .catch(error => console.error("Error deleting item:", error));

}


window.onload = fetchItems; 
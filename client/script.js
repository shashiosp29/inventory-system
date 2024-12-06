function fetchItems() {
    fetch('/api/items')
        .then(response => response.json())
        .then(data => {
            const itemList = document.getElementById('itemList');
            itemList.innerHTML = ''; // Clear existing items
            data.forEach(item => { // Corrected loop
                const listItem = document.createElement('li');
                listItem.textContent = `${item[1]} - Quantity: ${item[2]}` + "  "; // Access by index since now data is array of arrays

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => deleteItem(item[0]); // Access id by index

                listItem.appendChild(deleteButton);
                itemList.appendChild(listItem);

            });

        })
        .catch(error => console.error("Error fetching items:", error));

}


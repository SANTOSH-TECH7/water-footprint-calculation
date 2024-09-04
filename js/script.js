// Function to handle sending message and receiving response
async function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatlogs = document.querySelector('.chatlogs');

    // Display user message
    chatlogs.innerHTML += `<div class="user-message">${userInput}</div>`;
    document.getElementById('userInput').value = '';

    // Prepare request data
    const [product_name, quantity] = userInput.split(',');
    
    // Make a POST request to Flask
    const response = await fetch('/get_water_footprint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_name: product_name.trim(),
            quantity: parseFloat(quantity.trim())
        })
    });

    const data = await response.json();
    const totalFootprint = data.total;

    // Display bot response
    chatlogs.innerHTML += `<div class="bot-response">Estimated Total Water Footprint: ${totalFootprint.toFixed(2)} liters</div>`;
}

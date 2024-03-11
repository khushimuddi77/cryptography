// Function to handle choosing an image
function chooseImage() {
    const fileInput = document.getElementById('fileInput');
    fileInput.click(); // Trigger click event on file input
}

// Function to handle uploading an image
// Function to handle uploading an image
// Function to handle uploading an image
function uploadImage() {
    const fileInput = document.getElementById('fileInput');

    // Check if a file was selected
    if (fileInput.files.length === 0) {
        alert('Please select an image.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    // Send image data to Flask server using fetch API or XMLHttpRequest
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle response from server, such as displaying original image
        const originalImage = document.getElementById('originalImage');
        originalImage.src = URL.createObjectURL(file); // Set src attribute to display the selected image
        originalImage.style.display = 'block'; // Show the image

        // Call encryptImage function with the uploaded image path
        // encryptImage(originalImage.src);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function encryptImage(imagePath) {
    // Send request to Flask server to encrypt the image
    fetch('/encrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'image_path': imagePath })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle response from server, such as displaying a success message or encrypted image path
        if (data.success) {
            console.log('Image encrypted successfully');
            console.log('Encrypted image path:', data.encrypted_image_path);

            // Call a function to display the encrypted image using its path
            displayEncryptedImage(data.encrypted_image_path);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// Example function to display the encrypted image
function displayEncryptedImage(imagePath) {
    // Example code to display the encrypted image using its path
    const encryptedImageElement = document.getElementById('encryptedImage');
    encryptedImageElement.src = imagePath;
    encryptedImageElement.style.display = 'block'; // Make sure the image is visible
}

// Function to handle image decryption
// Function to handle image decryption
function decryptImage(imagePath) {
    // Send request to Flask server to decrypt the image
    fetch('/decrypt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'image_path': imagePath })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle response from server, such as displaying the decrypted image
        if (data.success) {
            console.log('Image decrypted successfully');
            console.log('Decrypted image path:', data.decrypted_image_path);
            
            // Call a function to display the decrypted image using its path
            displayDecryptedImage(data.decrypted_image_path);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
// Function to display the decrypted image
function displayDecryptedImage(imagePath) {
    // Get the image element by its ID
    const decryptedImageElement = document.getElementById('decryptedImage');

    // Set the src attribute of the image element to the decrypted image path
    decryptedImageElement.src = imagePath;

    // Make sure the image is visible
    decryptedImageElement.style.display = 'block';
}

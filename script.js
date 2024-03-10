// Function to handle uploading an image
function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const imageContainer = document.getElementById('imageContainer');
    
    // Trigger click event on file input
    fileInput.click();

    // Handle file selection
    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const img = new Image();
            img.src = e.target.result;

            img.onload = function() {
                // Display the original image
                const originalImage = document.getElementById('originalImage');
                originalImage.src = img.src;
                originalImage.style.display = 'block';
                
                // Hide ciphered and decrypted images
                document.getElementById('cipheredImage').style.display = 'none';
                document.getElementById('decryptedImage').style.display = 'none';
            }
        };

        reader.readAsDataURL(file);
    });
}


// Function to handle pasting an image URL or Base64 data
function pasteImage() {
    const imageTextarea = document.getElementById('imageTextarea');
    const imageContainer = document.getElementById('imageContainer');
    
    // Get the pasted image data from the textarea
    const imageData = imageTextarea.value;

    // Check if the pasted data is a valid image URL or Base64 data
    const isDataURL = /^data:image\/([a-zA-Z]*);base64,([^\/]+)$/.test(imageData);
    const isImageURL = /(https?:\/\/.*\.(?:png|jpg|jpeg|gif))/i.test(imageData);

    // If the pasted data is valid, display the image
    if (isDataURL || isImageURL) {
        const img = new Image();
        img.src = imageData;

        img.onload = function() {
            // Display the original image
            const originalImage = document.getElementById('originalImage');
            originalImage.src = img.src;
            originalImage.style.display = 'block';
            
            // Hide ciphered and decrypted images
            document.getElementById('cipheredImage').style.display = 'none';
            document.getElementById('decryptedImage').style.display = 'none';
        };
    } else {
        alert('Invalid image data. Please paste a valid image URL or Base64 data.');
    }
}

// Function to handle image encryption
function encryptImage() {
    // Implement your encryption algorithm here
    // Update ciphered image src and display it
    document.getElementById('cipheredImage').style.display = 'block';
}

// Function to handle image decryption
function decryptImage() {
    // Implement your decryption algorithm here
    // Update decrypted image src and display it
    document.getElementById('decryptedImage').style.display = 'block';
}

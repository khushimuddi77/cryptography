function chooseImage() {
    const fileInput = document.getElementById('fileInput');
    
    fileInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        
        if (selectedFile) {
            const fileName = selectedFile.name;
            const fileExtension = fileName.split('.').pop().toLowerCase();
            
            if (['jpg', 'jpeg', 'png'].includes(fileExtension)) {
                
              
            } else {
                alert('Please select a file with a valid extension (jpg, jpeg, png).');
            }
        }
    });
    
    fileInput.click();
}

function uploadImage() {
    const fileInput = document.getElementById('fileInput');

    if (fileInput.files.length === 0) {
        alert('Please select an image.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const originalImage = document.getElementById('originalImage');
        originalImage.src = data.image_path;
        originalImage.style.display = 'block'; 
        encryptImage(originalImage.src) 
        console.log("here")
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function encryptImage(imagePath) {

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
        if (data.success) {
            console.log('Image encrypted successfully');
            console.log('Encrypted image path:', data.encrypted_image_path);

            displayEncryptedImage(data.encrypted_image_path);
            decryptImage()
           
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function displayEncryptedImage(imagePath) {
    const encryptedImageElement = document.getElementById('encryptedImage');
    encryptedImageElement.src = imagePath;
    encryptedImageElement.style.display = 'block'; 
}


function decryptImage(imagePath) {
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
        if (data.success) {
            console.log('Image decrypted successfully');
            console.log('Decrypted image path:', data.decrypted_image_path);
            
            displayDecryptedImage(data.decrypted_image_path);
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function displayDecryptedImage(imagePath) {
    const decryptedImageElement = document.getElementById('decryptedImage');
    decryptedImageElement.src = imagePath;
    decryptedImageElement.style.display = 'block';
}



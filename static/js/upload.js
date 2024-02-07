
document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    // Show the loading animation
    document.getElementById('loadingAnimation').style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          // Hide the loading animation
          document.getElementById('loadingAnimation').style.display = 'none';
          
          // Display the OCR result
          document.getElementById('ocr-result').textContent = data.extracted_text;
      }).catch(error => {
          console.error('Error:', error);
          // Hide the loading animation in case of an error
          document.getElementById('loadingAnimation').style.display = 'none';
      });
});

// document.getElementById('upload-form').addEventListener('submit', function(e) {
//     e.preventDefault();
//     var formData = new FormData(this);

//     document.getElementById('loadingAnimation').style.display = 'block';
//     document.getElementById('image-preview').style.display = 'none';

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     }).then(response => response.json())
//       .then(data => {
//           document.getElementById('loadingAnimation').style.display = 'none';
//           document.getElementById('ocr-result').textContent = data.extracted_text;
//       }).catch(error => {
//           console.error('Error:', error);
//           document.getElementById('loadingAnimation').style.display = 'none';
//       });
// });

// document.getElementById('image-input').addEventListener('change', function(e) {
//     if (e.target.files && e.target.files[0]) {
//         var reader = new FileReader();
//         reader.onload = function(e) {
//             document.getElementById('image-preview').src = e.target.result;
//             document.getElementById('image-preview').style.display = 'block';
//         };
//         reader.readAsDataURL(e.target.files[0]);
//     }
// });
let extract_box = document.querySelector(".extract-box")
// extract_box.style.display = "none";
document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var formData = new FormData(this);

    // Show the loading animation
    
    let uploadBtn = ` <button type="submit" class="btn btn-primary text-center">Upload</button>`

    let loading_animation = ` <button class="btn btn-primary" type="button" disabled>
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">Loading...</span>`

    

    let loader = document.querySelector(".hide_on_load")

    loader.innerHTML = loading_animation
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          // Hide the loading animation
          loader.innerHTML = uploadBtn
          
          extract_box.style.display = "flex";
          // Display the OCR result
          document.getElementById('ocr-result').textContent = data.extracted_text;
      }).catch(error => {
          console.error('Error:', error);
          // Hide the loading animation in case of an error
      });
});

// document.getElementById('upload-form').addEventListener('submit', function(e) 
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

// code for copy box
// Get the <pre> elementlet copyText = document.querySelector(".copy-text");
function copyText() {
    var textToCopy = document.getElementById("ocr-result");
    document.querySelector(".copybutton").innerHTML = "Copied!"
    
    // Select the text
    textToCopy.select();
    
    // Copy the selected text
    document.execCommand("copy");
    
    alert("Text copied!");
  }


  document.querySelector(".copybutton").addEventListener("click",(e)=>{
        let copyBtn = document.querySelector(".copybutton")
        copyBtn.innerHTML = "copied!!"
        setTimeout(()=>{
            copyBtn.innerHTML = "Copy"
        },3000)

        let extract_text = document.querySelector("#ocr-result");
        console.log(extract_text);
        navigator.clipboard.writeText(extract_text)
  })
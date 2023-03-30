const  events = ['dragenter', 'dragover', 'dragleave', 'drop'];
const dropArea=document.getElementById("drop-area");
const csrfmiddlewaretoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const gallery = document.getElementById("gallery");
const allowedExtensions = [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/gif',

]

let globalSrc = '';
const validExtensions = (extension, allowedExtensions) => {
    return allowedExtensions.includes(extension);
}

const viewImage = src => { 
    console.log('src: ', src)
    const img = document.createElement('img');
    globalSrc = src;
    img.src = src;
    const a = document.createElement('a');
    a.href=src;
    console.log('a child element', a.childElementCount)
    a.appendChild(img);
    if (gallery.childElementCount > 0) {
        console.log('here')
        gallery.replaceChild(a, gallery.children[0])
    } else {
        gallery.appendChild(a);
    }   
}

const uploadFiles = files => {
    const url = '/upload_file/';
    let formData = new FormData();
    formData.append('file', files[0]);
    console.log('file: ', formData);
    fetch(url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        }, 
        body: formData
    })
    .then(response => {
        return response.json();
    })
    .then(data => { // for viewing files
        console.log('data: ', data);
        [...data].forEach(file=>viewImage(file));
    })
    .catch(error => {
        console.log(error);
    })
}

const highlight = () => {
    dropArea.classList.add('highlight')
}

const unhighlight = () => {
    dropArea.classList.remove('highlight')
}
const preventDefaultBehaviour = event=> {
    event.preventDefault();
    event.stopPropagation();
}
const handleFiles = files => {
    console.log(files.length)
    let valid = true;
    if(files.length>1) {
        alert('Upload only one file')
    } else {
        console.log('file type', files[0].type)
        if(! validExtensions(files[0].type, allowedExtensions)) {
            valid = false;    
        }
        if(valid) {
            console.log(files[0].type)
            uploadFiles(files);
        } else {
            alert('Invalid format')
        }
    }  
}
const handleDrop = event => {
    const files=event.dataTransfer.files;
    handleFiles(files)
}

function submitImage() {
    if (globalSrc) {
        alert('image submitted') 
    } else {
        alert('Select an Image');    
    }
}
events.forEach(event=> {
    dropArea.addEventListener(event, preventDefaultBehaviour)
})

events.slice(0,2).forEach(event => {
    dropArea.addEventListener(event, highlight)
})
events.slice(2,).forEach(event => {
    dropArea.addEventListener(event, unhighlight)
})

dropArea.addEventListener('drop', handleDrop);




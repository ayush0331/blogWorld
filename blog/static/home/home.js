function detectFile(){
    var fileElement = document.getElementById("newPostFile");
    var fileElementName = document.getElementById("newPostFileName");
    fileElementName.innerText = "";
    if (fileElement.files.length){
        var fileObj = fileElement.files[0];
        if (fileObj.type == "image/jpeg"){
            if (fileObj.size > 2000000){
                fileElement.value = "";
                alert("file size must be less than 2MB");
            }else {
                fileElementName.innerText = "("+fileObj.name+")"
            }
        }else {
            fileElement.value = "";
            alert("invalid file type");
        }

    }else {fileElement.value = "";}
}
document.getElementById("newPostFile").addEventListener("change",detectFile);
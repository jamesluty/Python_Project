const cloudName = "baby-to-baby"
const uploadPreset = "ex4bjxe6"

const myWidget = cloudinary.createUploadWidget({
    cloudName: cloudName,
    uploadPreset: uploadPreset},

    (error, result) => {
        if (!error && result && result.event === "success") {
            console.log('Done! Here is the image info: ', result.info);
            document
                .getElementById("upload_widget")
                .setAttribute("type", "hidden")
            document
                .getElementById("imgUrl")
                .setAttribute("value", result.info.secure_url);
            document
                .getElementById("uploadedimage")
                .setAttribute("src", result.info.secure_url);
        }
    }
)

document.getElementById("upload_widget").addEventListener("click", function(){
    myWidget.open();
}, false,);




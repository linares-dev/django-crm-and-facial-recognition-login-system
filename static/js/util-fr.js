const video = document.getElementById("video");
const videoCanvas = document.getElementById("video-canvas");

// load models
Promise.all([
    faceapi.nets.ssdMobilenetv1.loadFromUri("/static/js/models")
    ,faceapi.nets.faceRecognitionNet.loadFromUri("/static/js/models")
    ,faceapi.nets.faceLandmark68Net.loadFromUri("/static/js/models")
]).then(startWebCam).then(faceRecognition);

function startWebCam(){
    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
    }).then((stream)=>{
        video.srcObject = stream;
    }).catch((error) =>{
    console.error(error);
    });
}

function getLabeledFaceDescriptions(){
    const labels = ["ali.jpeg","paco.jpg"]
    return Promise.all( labels.map(async (label) => {
            const descriptions = []
            for(i=1;i<=5;i++){
                const image = await faceapi.fetchImage(`/media/images/${label}`);
                const detections = await faceapi
                .detectSingleFace(image)
                .withFaceLandmarks()
                .withFaceDescriptor();

                descriptions.push(detections.descriptor);
            }
            return new faceapi.LabeledFaceDescriptors(label,descriptions)
        })
    );
}

async function faceRecognition(){
    const labeledFaceDescriptors = await getLabeledFaceDescriptions();
    const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors);
    video.addEventListener("playing",()=>{
        location.reload();
    });
        const canvas =  faceapi.createCanvasFromMedia(video);
        videoCanvas.append(canvas);

        const displaySize = {width: video.width,height:video.height}
        faceapi.matchDimensions(canvas,displaySize);

        setInterval(async ()=>{
            const detections = await faceapi
            .detectAllFaces(video)
            .withFaceLandmarks()
            .withFaceDescriptors();

            const resizedDetections = faceapi.resizeResults(detections,displaySize);

            canvas.getContext("2d").clearRect(0,0,canvas.width,canvas.height);

            const results = resizedDetections.map((detected)=>{
                console.log(faceMatcher.findBestMatch(detected.descriptor));
                return faceMatcher.findBestMatch(detected.descriptor);
            });

            results.forEach((result,i) => {
                const box = resizedDetections[i].detection.box;
                const drawBox = new faceapi.draw.DrawBox(box,{label:result});
                drawBox.draw(canvas);
            });
        },100);
}

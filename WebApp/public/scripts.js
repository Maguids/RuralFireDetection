// Global variables
let selectedModel = null;
let tfModel = null;
const modelInputSizes = { model_1: 224, model_2: 256 };
let currentImage = null;
let imageSource = null;
const analysisHistory = [];
const MAX_HISTORY_ITEMS = 5;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileUpload = document.getElementById('file-upload');
const analyzeBtn = document.getElementById('analyze-btn');
const removeImageBtn = document.getElementById('remove-image-btn');
const dropzoneContent = document.getElementById('dropzone-content');
const imagePreview = document.getElementById('image-preview');
const imageSourceText = document.getElementById('image-source');
const resultContainer = document.getElementById('result-container');
const resultsContent = document.getElementById('results-content');
const selectedModelDisplay = document.getElementById('selected-model');

// Event Listeners
fileUpload.addEventListener('change', handleFileSelect);
dropzone.addEventListener('dragover', handleDragOver);
dropzone.addEventListener('dragleave', handleDragLeave);
dropzone.addEventListener('drop', handleDrop);
analyzeBtn.addEventListener('click', analyzeImage);
removeImageBtn.addEventListener('click', removeImage);

// Functions
function togglePhase(phaseId) {
    const models = document.getElementById(`${phaseId}-models`);
    const arrow = document.getElementById(`${phaseId}-arrow`);

    models.classList.toggle('hidden');
    arrow.classList.toggle('rotate-180');
}


function selectModel(phase, modelName) {
    selectedModel = { phase, modelName };
    selectedModelDisplay.textContent = `${phase} - ${modelName}`;

    document.querySelectorAll('.model-card').forEach(card => {
        card.classList.remove('ring-2', 'ring-orange-500');
    });

    event.currentTarget.classList.add('ring-2', 'ring-orange-500');

    if (currentImage) {
        analyzeBtn.disabled = false;
    }}


function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.match('image.*')) {
        processImage(file, 'Uploaded file');
    }
}

function handleDragOver(event) {
    event.preventDefault();
    dropzone.classList.add('active');
}

function handleDragLeave() {
    dropzone.classList.remove('active');
}

function handleDrop(event) {
    event.preventDefault();
    dropzone.classList.remove('active');

    const file = event.dataTransfer.files[0];
    if (file && file.type.match('image.*')) {
        processImage(file, 'Dropped file');
    }
}

function processImage(file, source) {
    const reader = new FileReader();

    reader.onload = function(e) {
        currentImage = e.target.result;
        imageSource = source;

        // Display preview in dropzone
        imagePreview.src = currentImage;
        dropzoneContent.classList.add('hidden');
        imagePreview.classList.remove('hidden');
        imageSourceText.textContent = source;
        imageSourceText.classList.remove('hidden');

        // Enable analyze button if model is selected and show remove button
        if (selectedModel) {
            analyzeBtn.disabled = false;
        }
        removeImageBtn.classList.remove('hidden');

        // Clear previous results
        resultContainer.classList.remove('show');
        resultsContent.innerHTML = '';
    };

    reader.readAsDataURL(file);
}

function toggleSamples(dataset) {
  const section = document.getElementById(`${dataset}Samples`);
  const arrow = document.getElementById(`${dataset}-arrow`);

  section.classList.toggle("hidden");
  arrow.classList.toggle("rotate-180");
}

function useSampleImage(imageName, dataset) {
    currentImage = `/ImageSamples/${imageName}`;
    imageSource = `Sample: ${imageName}`;

    // Display preview in dropzone
    imagePreview.src = currentImage;
    dropzoneContent.classList.add('hidden');
    imagePreview.classList.remove('hidden');
    imageSourceText.textContent = imageSource;
    imageSourceText.classList.remove('hidden');

    // Enable analyze button if model is selected and show remove button
    if (selectedModel) {
        analyzeBtn.disabled = false;
    }
    removeImageBtn.classList.remove('hidden');

    // Clear previous results
    resultContainer.classList.remove('show');
    resultsContent.innerHTML = '';
}

function removeImage() {
    currentImage = null;
    imageSource = null;
    fileUpload.value = '';

    // Hide preview and show dropzone content
    dropzoneContent.classList.remove('hidden');
    imagePreview.classList.add('hidden');
    imageSourceText.classList.add('hidden');

    // Disable analyze button
    analyzeBtn.disabled = true;

    // Hide remove button
    removeImageBtn.classList.add('hidden');

    // Clear results
    resultContainer.classList.remove('show');
    resultsContent.innerHTML = '';
}

function addToHistory(result) {
    // Add to beginning of array
    analysisHistory.unshift(result);

    // Trim if exceeds max size
    if (analysisHistory.length > MAX_HISTORY_ITEMS) {
        analysisHistory.pop();
    }

    // Update display
    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    const container = document.getElementById('history-container');
    container.innerHTML = '';

    if (analysisHistory.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-4">No analysis history yet</p>';
        return;
    }

    analysisHistory.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'bg-gray-50 p-4 rounded-lg border border-gray-200';
        historyItem.innerHTML = `
            <div class="flex flex-col md:flex-row gap-4">
                <div class="flex-shrink-0">
                    <img src="${item.image}" alt="History image" class="w-24 h-24 object-cover rounded-lg">
                </div>
                <div class="flex-grow">
                    <div class="flex justify-between items-start">
                        <h3 class="font-medium">Analysis #${index + 1}</h3>
                        <span class="text-sm text-gray-500">${new Date(item.timestamp).toLocaleString()}</span>
                    </div>
                    <div class="mt-2 grid grid-cols-2 gap-2 text-sm">
                        <div>
                            <span class="text-gray-600">Model:</span>
                            <span>${item.model}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Result:</span>
                            <span class="${item.hasFire ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}">
                                ${item.hasFire ? 'Fire detected' : 'No fire'}
                            </span>
                        </div>
                        <div>
                            <span class="text-gray-600">Confidence:</span>
                            <span>${item.confidence}</span>
                        </div>
                        <div>
                            <span class="text-gray-600">Source:</span>
                            <span>${item.source}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(historyItem);
    });
}

        
async function analyzeImage() {
    if (!currentImage || !selectedModel) return;

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Analyzing...';

    const response = await fetch(currentImage);
    const blob = await response.blob();
    const formData = new FormData();
    formData.append('image', blob, 'image.jpg');
    formData.append('phase', selectedModel.phase);
    formData.append('modelName', selectedModel.modelName);

    try {
        const res = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const result = await res.json();
        const hasFire = result.hasFire;
        const confidence = result.confidence;

        resultsContent.innerHTML = `
            <div class="flex justify-between">
                <span class="font-medium">Model used:</span>
                <span>${selectedModel.phase} - ${selectedModel.modelName}</span>
            </div>
            <div class="flex justify-between">
                <span class="font-medium">Fire detected:</span>
                <span class="${hasFire ? 'text-red-600 font-bold' : 'text-green-600 font-bold'}">
                    ${hasFire ? 'YES' : 'NO'}
                </span>
            </div>
            <div class="flex justify-between">
                <span class="font-medium">Confidence:</span>
                <span>${confidence}</span>
            </div>
            <div class="mt-4 p-3 rounded-lg ${hasFire ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'}">
                <i class="fas ${hasFire ? 'fa-fire' : 'fa-check-circle'} mr-2"></i>
                ${hasFire ? 'Fire detected in the image!' : 'No fire detected in the image.'}
            </div>
        `;

        resultContainer.classList.add('show');

        addToHistory({
            image: currentImage,
            model: `${selectedModel.phase} - ${selectedModel.modelName}`,
            hasFire,
            confidence,
            source: imageSource,
            timestamp: new Date()
        });

    } catch (error) {
        console.error("Erro ao analisar imagem:", error);
        alert("Erro ao processar a imagem no servidor.");
    }

    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = 'Analyze Image';
}


// Initialize with phase 1 models open
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('phase1-models').classList.remove('hidden');
    document.getElementById('phase1-arrow').classList.add('rotate-180');
});

window.selectModel = selectModel;
window.useSampleImage = useSampleImage;
window.togglePhase = togglePhase;
window.toggleSamples = toggleSamples;


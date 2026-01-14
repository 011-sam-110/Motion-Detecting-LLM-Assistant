# Import the Roboflow and YOLO modules
from roboflow import Roboflow
from ultralytics import YOLO

# The 'Roboflow' module is used for working with datasets on the Roboflow platform
# The 'YOLO' module is imported from the 'ultralytics' library, which is used for YOLO object detection tasks

# Import the Roboflow library and create an instance with the provided API key
api_key = "your-api-key"
rf = Roboflow(api_key)

# Access the Roboflow workspace named "lazydevs"
# Access the project named "human-detection" within the workspace
workspace_name = "lazydevs"
project_name = "human-detection"
project = rf.workspace(workspace_name).project(project_name)

# Download the dataset associated with version 4 of the project using YOLOv8 format
# Note: You might want to include a specific version number or method for version selection.
version = 4
form = "yolov8"
dataset = project.version(version).download(form)

# Initialize the YOLO model by loading the pre-trained weights from 'yolov8n.pt'
model = YOLO('yolov8n.pt')

# Train the model with the specified parameters
results = model.train(
    data='/kaggle/input/v4-yaml/data.yaml',  # Path to the training data YAML file
    epochs=150,  # Number of training epochs
    batch=64,  # Batch size for ntraining
    imgsz=640,  # Input image size
    seed=32,  # Random seed for reproducibility
    optimizer='NAdam',  # Optimizer algorithm
    weight_decay=1e-4,  # Weight decay for regularization
    momentum=0.937,  # Initial momentum for the optimizer
    cos_lr=True,  # Use cosine learning rate scheduling
    lr0=0.01,  # Initial learning rate
    lrf=1e-5,  # Final learning rate
    warmup_epochs=10,  # Number of warmup epochs
    warmup_momentum=0.5,  # Momentum during warm-up epochs
    close_mosaic=20,  # Parameter for close mosaic augmentation
    label_smoothing=0.2,  # Label smoothing parameter for regularization
    dropout=0.5,  # Dropout rate to prevent overfitting
    verbose=True  # Print verbose training information
)
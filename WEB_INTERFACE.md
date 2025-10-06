# DeepWriting Web Interface

This web interface provides an easy-to-use platform for synthesizing handwriting from text using the DeepWriting model.

## Features

- **Text Input**: Enter any text you want to synthesize into handwriting
- **Style Selection**: Choose from predefined handwriting styles to mimic specific writing styles
- **Real-time Synthesis**: Generate handwritten text on-demand
- **SVG Output**: High-quality vector graphics output

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Download the pre-trained model:
```bash
# Download the model from:
# https://files.ait.ethz.ch/projects/deepwriting/tf-1514981744-deepwriting_synthesis_model.tar.gz

# Extract it to a directory, e.g., ./model/
tar -xzf tf-1514981744-deepwriting_synthesis_model.tar.gz
```

3. Ensure you have the validation dataset in the `data` folder:
```bash
# The model requires the validation dataset for statistics
# Download from: https://files.ait.ethz.ch/projects/deepwriting/deepwriting_dataset.zip
```

## Usage

### Starting the Web Server

Run the Flask application with the path to your model:

```bash
python app.py -M ./model/tf-1514981744-deepwriting_synthesis_model
```

Optional arguments:
- `-M, --model_path`: Path to model checkpoint directory (required)
- `-C, --config`: Path to configuration file (optional)
- `-P, --port`: Port to run the server on (default: 5000)
- `--host`: Host address (default: 0.0.0.0)

Example:
```bash
python app.py -M ./runs/tf-1514981744-deepwriting_synthesis_model -P 8080
```

### Accessing the Interface

Once the server is running, open your web browser and navigate to:
```
http://localhost:5000
```

### Using the Interface

1. **Enter Text**: Type or paste the text you want to synthesize in the text input field
2. **Select Style** (optional): Choose a handwriting style from the dropdown menu
   - Leave as "Random Style" for unbiased sampling with a random style
   - Select a specific style to mimic that particular handwriting
3. **Synthesize**: Click the "Synthesize Handwriting" button
4. **View Result**: The synthesized handwriting will appear below as an SVG image

### Quick Examples

The interface provides several quick example texts you can try:
- "Hello, World!"
- "The quick brown fox jumps over the lazy dog."
- "I am a synthetic sample."
- "This is handwriting synthesis."

## API Endpoints

The web interface also exposes REST API endpoints:

### POST /api/synthesize
Synthesize handwriting from text.

**Request Body:**
```json
{
  "text": "Text to synthesize",
  "style_id": 107  // Optional, for biased sampling
}
```

**Response:**
```json
{
  "success": true,
  "svg": "<svg>...</svg>"
}
```

### GET /api/styles
Get available handwriting styles.

**Response:**
```json
{
  "styles": [
    {"id": 107, "name": "Style 1"},
    {"id": 226, "name": "Style 2"},
    {"id": 696, "name": "Style 3"}
  ]
}
```

## Troubleshooting

### Model Not Loading
- Ensure the model path is correct and contains checkpoint files
- Verify that the validation dataset is available in the `data` folder
- Check that TensorFlow is properly installed

### Memory Issues
- The model requires significant GPU/CPU memory
- Reduce the `seq_len` parameter in the synthesis function if needed
- Ensure no other TensorFlow processes are running

### Synthesis Takes Too Long
- Synthesis time depends on text length and hardware
- Shorter texts synthesize faster
- GPU acceleration is recommended for faster synthesis

## Technical Details

### Sampling Methods

1. **Unbiased Sampling**: Generates handwriting with a random style
   - No reference sample needed
   - Style varies each time

2. **Biased Sampling**: Mimics a specific handwriting style
   - Uses a reference sample from the validation dataset
   - Consistent style based on the selected sample

### Parameters

Key synthesis parameters (can be modified in `app.py`):
- `seq_len`: Maximum sequence length (default: 800)
- `eoc_threshold`: End-of-character threshold (default: 0.05)
- `cursive_threshold`: Cursive writing threshold (default: 0.005)
- `use_sample_mean`: Use mean instead of sampling from distribution (default: True)

## Citation

If you use this interface or the DeepWriting model, please cite the original paper:

```
@inproceedings{Aksan:2018:DeepWriting,
    author = {Aksan, Emre and Pece, Fabrizio and Hilliges, Otmar},
    title = {{DeepWriting: Making Digital Ink Editable via Deep Generative Modeling}},
    booktitle = {SIGCHI Conference on Human Factors in Computing Systems},
    series = {CHI '18},
    year = {2018},
    location = {Montr{\'e}al, Canada},
    publisher = {ACM},
    address = {New York, NY, USA},
}
```

## License

This web interface is provided as an extension to the DeepWriting project. Please refer to the main LICENSE file for licensing information.

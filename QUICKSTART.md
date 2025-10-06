# Quick Start Guide - DeepWriting Web Interface

Get up and running with the handwriting synthesis web interface in 5 minutes!

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- 4GB+ RAM (8GB recommended)
- GPU (optional, but recommended for faster synthesis)

## Step 1: Install Dependencies

```bash
cd /path/to/deepwriting
pip install -r requirements.txt
```

**Note**: This will install Flask, TensorFlow, NumPy, OpenCV, and other required packages.

## Step 2: Download the Pre-trained Model

Download and extract the model:

```bash
# Create a directory for the model
mkdir -p model

# Download the model (if not already downloaded)
wget https://files.ait.ethz.ch/projects/deepwriting/tf-1514981744-deepwriting_synthesis_model.tar.gz

# Extract
tar -xzf tf-1514981744-deepwriting_synthesis_model.tar.gz -C model/
```

## Step 3: Download the Validation Dataset

The model needs the validation dataset for statistics:

```bash
# Create data directory
mkdir -p data

# Download validation data (if not already downloaded)
wget https://files.ait.ethz.ch/projects/deepwriting/deepwriting_dataset.zip

# Extract
unzip deepwriting_dataset.zip
mv deepwriting_validation.npz data/
```

## Step 4: Test Your Setup

Verify everything is installed correctly:

```bash
python test_web_interface.py
```

Expected output:
```
============================================================
Web Interface Component Tests
============================================================
Testing imports...
✓ Flask imported successfully
✓ NumPy imported successfully
✓ svgwrite imported successfully
✓ OpenCV imported successfully

Testing Flask app creation...
✓ Flask app created successfully
✓ Template file exists: templates/index.html

Testing SVG generation...
✓ SVG generation successful

============================================================
✓ All tests passed!

To start the web interface (requires trained model):
  python app.py -M <path_to_model_checkpoint>
============================================================
```

## Step 5: Start the Web Server

```bash
python app.py -M ./model/tf-1514981744-deepwriting_synthesis_model
```

Expected output:
```
Loading model...
Model restored from ./model/tf-1514981744-deepwriting_synthesis_model/model.ckpt-XXXXX
Model loaded successfully!
Starting server on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Step 6: Access the Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

You should see the DeepWriting interface!

## Step 7: Synthesize Your First Handwriting

1. In the text input field, type: `Hello, World!`
2. Leave the style as "Random Style (Unbiased)"
3. Click "✨ Synthesize Handwriting"
4. Wait a few seconds
5. See your synthesized handwriting appear below!

## Try Different Styles

1. Change the style dropdown to "Style 1", "Style 2", or "Style 3"
2. Enter new text
3. Click synthesize again
4. Compare the different handwriting styles!

## Command-Line Alternative

If you prefer command-line usage:

```bash
# Simple synthesis
python demo_synthesis.py -M ./model/tf-1514981744-deepwriting_synthesis_model -T "Hello, World!" -O output.svg

# With specific style
python demo_synthesis.py -M ./model/tf-1514981744-deepwriting_synthesis_model -T "Hello, World!" -S 107 -O styled_output.svg
```

## Troubleshooting

### "No checkpoint found" error
- Verify the model path is correct
- Ensure the extracted model directory contains `.ckpt` files
- Check that you're pointing to the checkpoint directory, not the tar.gz file

### "No module named 'XXX'" error
- Run `pip install -r requirements.txt` again
- Verify Python version is 3.6+
- Try using `pip3` instead of `pip`

### "validation_data not found" error
- Ensure `data/deepwriting_validation.npz` exists
- Update the path in `config.py` if using a different location

### Synthesis is very slow
- Use a machine with GPU for faster synthesis
- Reduce text length (shorter text = faster synthesis)
- Close other TensorFlow processes

### Port 5000 already in use
- Use a different port: `python app.py -M <model_path> -P 8080`
- Or stop the process using port 5000

## Next Steps

- Read [WEB_INTERFACE.md](WEB_INTERFACE.md) for detailed documentation
- Read [WEB_INTERFACE_VISUAL_GUIDE.md](WEB_INTERFACE_VISUAL_GUIDE.md) for interface details
- Explore API endpoints for programmatic access
- Customize synthesis parameters in `app.py`

## Need Help?

- Check the main [README.md](README.md) for general information
- Review the original paper for technical details
- Check existing issues on GitHub

## Success!

You're now ready to synthesize handwriting! Enjoy creating beautiful handwritten text with DeepWriting! 🎉

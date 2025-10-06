"""
Flask web application for handwriting synthesis.
Provides a web interface to synthesize handwriting from text input.
"""
import os
import sys
import json
import base64
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from io import BytesIO

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

from tf_dataset_hw import HandWritingDatasetConditionalTF
from tf_models_hw import HandwritingVRNNGmmModel
import visualize_hw as visualize
import config as config_module

app = Flask(__name__)

# Global variables to store model and session
model = None
sess = None
validation_dataset = None
config = None

def load_model(model_path, config_path=None):
    """
    Load the pre-trained handwriting synthesis model.
    
    Args:
        model_path: Path to the model checkpoint directory
        config_path: Optional path to config file
    """
    global model, sess, validation_dataset, config
    
    # Load configuration
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = config_module.main()
    
    # Set environment variable
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    
    # Load validation dataset for statistics
    validation_dataset = HandWritingDatasetConditionalTF(
        config['validation_data'], 
        var_len_seq=True, 
        use_bow_labels=config['use_bow_labels']
    )
    
    # Create TensorFlow session
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    sess = tf.Session(config=tf_config)
    
    # Build model
    batch_size = 1
    input_op = tf.placeholder(dtype=tf.float32, shape=[batch_size, None, validation_dataset.input_dims], name='input_sequences')
    input_seq_length_op = tf.placeholder(dtype=tf.int32, shape=[batch_size], name='input_seq_lengths')
    target_op = tf.placeholder(dtype=tf.float32, shape=[batch_size, None, validation_dataset.target_dims], name='target_sequences')
    
    model = HandwritingVRNNGmmModel(
        config=config,
        input_op=input_op,
        input_seq_length_op=input_seq_length_op,
        target_op=target_op,
        input_dims=validation_dataset.input_dims,
        target_dims=validation_dataset.target_dims,
        reuse=False,
        batch_size=batch_size,
        mode='sampling',
        data_processor=validation_dataset
    )
    
    # Restore model checkpoint
    saver = tf.train.Saver()
    ckpt = tf.train.get_checkpoint_state(model_path)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
        print(f"Model restored from {ckpt.model_checkpoint_path}")
    else:
        raise ValueError(f"No checkpoint found in {model_path}")
    
    return True

def synthesize_handwriting(text, style_sample_id=None, seq_len=800):
    """
    Synthesize handwriting from text input.
    
    Args:
        text: Text string to synthesize
        style_sample_id: Optional sample ID for style reference (biased sampling)
        seq_len: Maximum sequence length
        
    Returns:
        SVG string of synthesized handwriting
    """
    global model, sess, validation_dataset
    
    if model is None or sess is None:
        raise ValueError("Model not loaded. Call load_model() first.")
    
    # Prepare keyword arguments
    keyword_args = {
        'conditional_inputs': text,
        'eoc_threshold': 0.05,
        'cursive_threshold': 0.005,
        'use_sample_mean': True
    }
    
    # Perform sampling
    if style_sample_id is not None:
        # Biased sampling with style reference
        _, stroke_sample, _ = validation_dataset.fetch_sample(style_sample_id)
        reference_sample = validation_dataset.normalize_sample(stroke_sample[0])
        
        # Run inference on reference sample
        feed = {
            model.inputs: np.expand_dims(reference_sample, axis=0),
            model.input_seq_length: np.array([reference_sample.shape[0]]),
            model.initial_state: sess.run(model.cell.zero_state(batch_size=1, dtype=tf.float32))
        }
        inference_results = sess.run(model.ops_evaluation, feed)
        
        # Sample with style
        sampling_results = model.sample_biased(
            session=sess,
            seq_len=seq_len,
            prev_state=inference_results['state'],
            prev_sample=reference_sample,
            **keyword_args
        )
    else:
        # Unbiased sampling (random style)
        sampling_results = model.sample_unbiased(
            session=sess,
            seq_len=seq_len,
            **keyword_args
        )
    
    # Convert to absolute coordinates
    synthetic_sample = validation_dataset.undo_normalization(
        sampling_results[0]['output_sample'][0],
        detrend_sample=False
    )
    
    # Generate SVG
    svg_path = '/tmp/temp_output.svg'
    visualize.draw_stroke_svg(synthetic_sample, factor=0.001, svg_filename=svg_path)
    
    # Read SVG content
    with open(svg_path, 'r') as f:
        svg_content = f.read()
    
    # Clean up
    if os.path.exists(svg_path):
        os.remove(svg_path)
    
    return svg_content

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/synthesize', methods=['POST'])
def api_synthesize():
    """
    API endpoint to synthesize handwriting.
    
    Expected JSON input:
    {
        "text": "Text to synthesize",
        "style_id": 107  (optional, for biased sampling)
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        style_id = data.get('style_id', None)
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Synthesize handwriting
        svg_content = synthesize_handwriting(text, style_id)
        
        return jsonify({
            'success': True,
            'svg': svg_content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/styles', methods=['GET'])
def api_styles():
    """
    Get list of available style samples.
    """
    try:
        # Return some predefined style sample IDs
        styles = [
            {'id': 107, 'name': 'Style 1'},
            {'id': 226, 'name': 'Style 2'},
            {'id': 696, 'name': 'Style 3'},
        ]
        return jsonify({'styles': styles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Handwriting Synthesis Web Interface')
    parser.add_argument('-M', '--model_path', type=str, required=True,
                        help='Path to model checkpoint directory')
    parser.add_argument('-C', '--config', type=str, default=None,
                        help='Path to configuration file (optional)')
    parser.add_argument('-P', '--port', type=int, default=5000,
                        help='Port to run the server on')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host address')
    
    args = parser.parse_args()
    
    # Load model
    print("Loading model...")
    load_model(args.model_path, args.config)
    print("Model loaded successfully!")
    
    # Run Flask app
    print(f"Starting server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)

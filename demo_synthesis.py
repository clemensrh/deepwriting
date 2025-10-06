#!/usr/bin/env python
"""
Example script showing how to use the handwriting synthesis API programmatically.
This demonstrates the API without requiring the web interface.

Usage:
    python demo_synthesis.py -M <model_path> -T "Your text here"
"""
import sys
import os
import argparse

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

import numpy as np
import tensorflow as tf
from tf_dataset_hw import HandWritingDatasetConditionalTF
from tf_models_hw import HandwritingVRNNGmmModel
import visualize_hw as visualize
import config as config_module

def load_model(model_path):
    """
    Load the pre-trained handwriting synthesis model.
    
    Args:
        model_path: Path to the model checkpoint directory
        
    Returns:
        model, session, validation_dataset, config
    """
    # Load configuration
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
    
    return model, sess, validation_dataset, config

def synthesize_unbiased(model, sess, validation_dataset, text, output_path, seq_len=800):
    """
    Synthesize handwriting with random style (unbiased sampling).
    
    Args:
        model: The loaded model
        sess: TensorFlow session
        validation_dataset: Dataset object
        text: Text to synthesize
        output_path: Path to save SVG output
        seq_len: Maximum sequence length
    """
    print(f"\nSynthesizing (unbiased): '{text}'")
    
    keyword_args = {
        'conditional_inputs': text,
        'eoc_threshold': 0.05,
        'cursive_threshold': 0.005,
        'use_sample_mean': True
    }
    
    # Perform unbiased sampling
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
    visualize.draw_stroke_svg(synthetic_sample, factor=0.001, svg_filename=output_path)
    print(f"✓ Saved to: {output_path}")

def synthesize_biased(model, sess, validation_dataset, text, style_id, output_path, seq_len=800):
    """
    Synthesize handwriting with specific style (biased sampling).
    
    Args:
        model: The loaded model
        sess: TensorFlow session
        validation_dataset: Dataset object
        text: Text to synthesize
        style_id: Sample ID for style reference
        output_path: Path to save SVG output
        seq_len: Maximum sequence length
    """
    print(f"\nSynthesizing (biased, style {style_id}): '{text}'")
    
    keyword_args = {
        'conditional_inputs': text,
        'eoc_threshold': 0.05,
        'cursive_threshold': 0.005,
        'use_sample_mean': True
    }
    
    # Get reference sample
    _, stroke_sample, _ = validation_dataset.fetch_sample(style_id)
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
    
    # Convert to absolute coordinates
    synthetic_sample = validation_dataset.undo_normalization(
        sampling_results[0]['output_sample'][0],
        detrend_sample=False
    )
    
    # Generate SVG
    visualize.draw_stroke_svg(synthetic_sample, factor=0.001, svg_filename=output_path)
    print(f"✓ Saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Handwriting Synthesis Demo')
    parser.add_argument('-M', '--model_path', type=str, required=True,
                        help='Path to model checkpoint directory')
    parser.add_argument('-T', '--text', type=str, default='Hello, World!',
                        help='Text to synthesize')
    parser.add_argument('-S', '--style_id', type=int, default=None,
                        help='Style sample ID for biased sampling (optional)')
    parser.add_argument('-O', '--output', type=str, default='output.svg',
                        help='Output SVG file path')
    parser.add_argument('-L', '--seq_len', type=int, default=800,
                        help='Maximum sequence length')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Handwriting Synthesis Demo")
    print("=" * 60)
    
    # Load model
    print("\nLoading model...")
    model, sess, validation_dataset, config = load_model(args.model_path)
    print("✓ Model loaded successfully!")
    
    # Synthesize
    if args.style_id is not None:
        synthesize_biased(model, sess, validation_dataset, args.text, args.style_id, args.output, args.seq_len)
    else:
        synthesize_unbiased(model, sess, validation_dataset, args.text, args.output, args.seq_len)
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
    
    # Clean up
    sess.close()

if __name__ == '__main__':
    main()

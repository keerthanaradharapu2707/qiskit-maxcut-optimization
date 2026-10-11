"""Noise analysis extension point; no hardware calibration data is fabricated."""

def describe_noise_status(processor_config):
    if processor_config.get("noise_model"):
        return "Configured noise model supplied; validate its provenance."
    return "No noise model configured. Results are ideal/local simulator results, not hardware predictions."

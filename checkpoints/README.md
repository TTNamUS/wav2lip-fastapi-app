# Model Checkpoints

This folder stores the Wav2Lip model files required for lip-syncing.  
**Model files are not included in the repository.**

### Download with gdown

1. Install gdown:
   ```sh
   uv pip install gdown
   ```

2. Download the model to the `checkpoints/` directory:
   ```sh
   uv run -m gdown 'https://drive.google.com/uc?id=1_OvqStxNxLc7bXzlaVG5sz695p-FVfYY' -O checkpoints/Wav2Lip.pth
   ```

For more model checkpoint options, see [app/models/Wav2Lip/README.md](../app/models/Wav2Lip/README.md) for details.
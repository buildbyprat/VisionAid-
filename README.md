# Model Directory

Place your pre-trained CNN model here:

    app/models/visionid_v1.h5

## Model Requirements
- Input:  (None, 224, 224, 3) — RGB image normalised to [0, 1]
- Output: (None, 5) — softmax probabilities for 5 classes:
  0. No DR
  1. Mild NPDR
  2. Moderate NPDR
  3. Severe NPDR
  4. Proliferative DR

If the model file is absent, the AI service runs in **demo mode**
and returns a random plausible prediction so the UI still works.

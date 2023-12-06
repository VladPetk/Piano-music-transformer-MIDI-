# Solo piano music transformer
A transformer model for generating solo piano compositions trained on a subset of [MMD data](https://github.com/jeffreyjohnens/MetaMIDIDataset "MMD data").

The best performing version uses REMI tokenization and byte-pair encoding (BPE). While it achieves lower accuracy (~70%) on the validation data than a model without BPE (~80%), the output is much more musical and coherent. The lower accuracy also makes sense given that the model with BPE has a vocabularly size of 2000 compared to 363 without BPE.
## Special thanks to:
- **lucidrains** for creating a powerful and convenient transformer library [x-transformers](https://github.com/lucidrains/x-transformers "x-transformers")
- **asigalov61** for implementation of x-transformers ([Allegro Music Transformer](https://github.com/asigalov61/Allegro-Music-Transformer "Allegro Music Transformer"))
- **feizc** for parts of the training code and data loader ([Perceiver-Music-Generation](https://github.com/feizc/Perceiver-Music-Generation "Perceiver-Music-Generation"))
- **lucidrain** for implementation of the [Perceiver AR architecture](https://github.com/lucidrains/perceiver-ar-pytorch "Perceiver AR architecture for symbolic music generation")
- **Natooz** for creation of the MIDI tokenization library [miditok](https://github.com/Natooz/MidiTok/tree/main/miditok "miditok")

## The journey
I tested out multiple models and tokenization techniques to see which one is the most promising:
1. X Transformer without BPE (Structured tokenization)
2. X Transformer with BPE (Structured tokenization)
3. Perceiver AR without BPE (Structured tokenization)
4. Perceiver AR with BPE (Structured tokenization)

Based on the results of these four models, I found that X Transformer performs better than Perceiver AR for this task. While Perceiver AR allowed for a much longer *maximum sequence length* on the same hardware compared to X Transformer (*4096 vs 1024*), the results were not encouraging in terms subjective evaluation of the generated output.  Consequently, I proceeded with the X Transformer architecture, testing the following models:

5. X transformer without BPE - larger model (Structured tokenization)
6. X transformer with BPE - larger model (Structured tokenization)
7. X transformer without BPE - larger model (REMI tokenization)
8. X transformer with BPE - larger model (REMI tokenization)

Two things stood out here: (1) REMI tokenization resulted in better rhythmic patterns: the generated music generally had more regular rhythm both within and across bars. (2) BPE resulted in more coherent music where musical ideas (motifs) are carried and repeated at  various points in the generated piece (with variations). This could be attributed to two factors, in my opinion: first, BPE can capture recurring musical motifs or phrases, enabling the model to represent more complex musical structures; and BPE effectively extends the maximum sequence length through data compression (with BPE vocab of 2000, the compression rate was ~0.52).

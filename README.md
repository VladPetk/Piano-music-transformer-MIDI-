#Solo piano music transformer
A transformer model for generating solo piano compositions trained on a subset of [MMD data](https://github.com/jeffreyjohnens/MetaMIDIDataset "MMD data").

The best performing version uses REMI tokenization and byte-pair encoding (BPE). While it achieves lower accuracy (~70%) on the validation data than a model without BPE (~80%), the output is much more musical and coherent. The lower accuracy also makes sense given that the model with BPE has a vocabularly size of 2000 compared to 363 without BPE.
## Special thanks to:
- **lucidrains** for creating a powerful and convenient transformer library [x-transformers](https://github.com/lucidrains/x-transformers "x-transformers")
- **asigalov61** for implementation of x-transformers ([Allegro Music Transformer](https://github.com/asigalov61/Allegro-Music-Transformer "Allegro Music Transformer"))
- **feizc** for parts of the training code and data loader ([Perceiver-Music-Generation](https://github.com/feizc/Perceiver-Music-Generation "Perceiver-Music-Generation"))
- **lucidrain** for implementation of the [Perceiver AR architecture](https://github.com/lucidrains/perceiver-ar-pytorch "Perceiver AR architecture for symbolic music generation")
- **Natooz** for creation of the MIDI tokenization library [miditok](https://github.com/Natooz/MidiTok/tree/main/miditok "miditok")

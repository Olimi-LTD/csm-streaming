from generator import load_csm_1b, Segment
import torchaudio

generator = load_csm_1b("cuda")

# Process audio chunks as they're generated
for audio_chunk in generator.generate_stream(
    text="This is generated chunk by chunk.",
    speaker=0,
    context=[]
):
    # Do something with each chunk as it's generated
    print(f"Received chunk of size: {audio_chunk.shape}")
    
    # You could process or play each chunk here
    # For example, write to a file incrementally
    # Or send over a network connection

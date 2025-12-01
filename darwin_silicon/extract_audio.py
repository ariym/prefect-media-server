from prefect import flow, task

@task
def validate_input():
    print("Step 1: Validating input.")

@task
def load_audio_file():
    print("Step 2: Loading audio file.")

@task
def extract_audio_stream():
    print("Step 3: Extracting audio stream.")

@task
def save_extracted_audio():
    print("Step 4: Saving extracted audio.")

@flow
def audio_extraction_flow():
    validate_input()
    load_audio_file()
    extract_audio_stream()
    save_extracted_audio()
    print("Audio extraction flow completed.")

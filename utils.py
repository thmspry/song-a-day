import base64

def encode_audio_to_base64(filepath: str) -> str:
    with open(filepath, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_output = base64_encoded_data.decode('utf-8')
        return base64_output
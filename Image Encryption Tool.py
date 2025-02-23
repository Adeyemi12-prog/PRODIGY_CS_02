from PIL import Image
import numpy as np
import random
import os
import base64

def generate_key():
    """Generate a unique encryption key."""
    key = os.urandom(16)  # 16-byte random key
    return base64.urlsafe_b64encode(key).decode()

def generate_seed(key):
    """Convert the encryption key to an integer seed."""
    return sum(bytearray(key.encode('utf-8')))

def encrypt_image(image_path):
    """Encrypt an image using pixel manipulation."""
    choice = input("Do you want to generate a new encryption key? (yes/no): ").strip().lower()
    
    if choice == "yes":
        key = generate_key()
        print(f"Generated Encryption Key: {key}")
    else:
        key = input("Enter your encryption key: ").strip()
    
    img = Image.open(image_path)
    img = img.convert("RGB")
    img_array = np.array(img, dtype=np.uint8)  # Ensure color depth remains consistent
    h, w, c = img_array.shape
    
    seed = generate_seed(key)
    random.seed(seed)
    
    indices = list(range(h * w))
    shuffled_indices = indices[:]
    random.shuffle(shuffled_indices)
    
    img_flattened = img_array.reshape(-1, 3)
    encrypted_img = np.zeros_like(img_flattened)
    
    mapping = dict(zip(indices, shuffled_indices))
    
    for i in indices:
        encrypted_img[mapping[i]] = img_flattened[i]
    
    encrypted_img = encrypted_img.reshape(h, w, 3)
    encrypted_img = Image.fromarray(encrypted_img.astype(np.uint8))
    
    ext = os.path.splitext(image_path)[1]
    encrypted_path = f"encrypted{ext}"
    encrypted_img.save(encrypted_path)
    print(f"Image encrypted successfully! Saved as '{encrypted_path}'")
    print(f"Use this key to decrypt the image: {key}")
    
    decrypt_choice = input("Do you want to decrypt the image now? (yes/no): ").strip().lower()
    if decrypt_choice == "yes":
        decrypt_image(encrypted_path)
    
    restart()

def decrypt_image(encrypted_path):
    """Decrypt an encrypted image using the same key."""
    key = input("Enter the encryption key: ").strip()
    
    img = Image.open(encrypted_path)
    img = img.convert("RGB")
    encrypted_img = np.array(img, dtype=np.uint8)  # Ensure original color retention
    h, w, c = encrypted_img.shape
    
    seed = generate_seed(key)
    random.seed(seed)
    
    indices = list(range(h * w))
    shuffled_indices = indices[:]
    random.shuffle(shuffled_indices)
    
    encrypted_flattened = encrypted_img.reshape(-1, 3)
    decrypted_img = np.zeros_like(encrypted_flattened)
    
    mapping = dict(zip(shuffled_indices, indices))
    
    for i in shuffled_indices:
        decrypted_img[mapping[i]] = encrypted_flattened[i]
    
    decrypted_img = decrypted_img.reshape(h, w, 3)
    decrypted_img = Image.fromarray(decrypted_img.astype(np.uint8))
    
    ext = os.path.splitext(encrypted_path)[1]
    decrypted_path = f"decrypted{ext}"
    decrypted_img.save(decrypted_path)
    print(f"Image decrypted successfully! Saved as '{decrypted_path}'")
    
    restart()

def restart():
    """Ask the user if they want to restart the process."""
    again = input("Do you want to perform another encryption or decryption? (yes/no): ").strip().lower()
    if again == "yes":
        main()
    else:
        print("Process completed. Exiting.")
        exit()

def main():
    print("Welcome to the Samurai Image Encryption Tool")
    print("This tool allows you to encrypt and decrypt images securely using a unique key.")
    print("Ensure to keep your encryption key safe, as it's required for decryption.")
    
    action = input("Do you want to encrypt or decrypt an image? (encrypt/decrypt): ").strip().lower()
    if action == "encrypt":
        image_path = input("Enter the path of the image to encrypt: ").strip()
        encrypt_image(image_path)
    elif action == "decrypt":
        image_path = input("Enter the path of the image to decrypt: ").strip()
        decrypt_image(image_path)
    else:
        print("Invalid choice. Please enter 'encrypt' or 'decrypt'.")
        main()

if __name__ == "__main__":
    main()

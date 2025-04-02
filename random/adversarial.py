import base64
import os
import random

def generate_random_base64_lines(num_lines):
    output = ""
    
    for _ in range(num_lines):
        # Generate random length between 30 and 500 bytes
        length = random.randint(30, 500)
        
        # Generate random bytes
        random_bytes = os.urandom(length)
        
        # Encode to base64
        base64_bytes = base64.b64encode(random_bytes)
        
        # Convert to string and add spaces every 4 characters
        base64_str = base64_bytes.decode('utf-8')
        spacing = random.randint(4, 500)
        spaced_base64 = ' '.join(base64_str[i:i+spacing] for i in range(0, len(base64_str), spacing))
        
        # Add to output with newline
        output += spaced_base64 + '\n'
    
    return output

# Generate and print 5 example lines
if __name__ == "__main__":
    result = generate_random_base64_lines(10000)
    print(result)
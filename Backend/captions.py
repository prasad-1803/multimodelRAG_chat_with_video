import re

# Function to parse a WEBVTT file
def parse_webvtt(vtt_file):
    captions = []
    
    # Regular expression to match timestamps
    timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})")
    
    with open(vtt_file, 'r') as file:
        lines = file.readlines()
        current_caption = {"start": None, "end": None, "text": ""}
        
        for line in lines:
            line = line.strip()
            
            # Check if line contains a timestamp
            timestamp_match = timestamp_pattern.match(line)
            if timestamp_match:
                # Save current caption if there's any text and reset
                if current_caption["text"]:
                    captions.append(current_caption)
                    current_caption = {"start": None, "end": None, "text": ""}
                
                # Extract start and end time
                current_caption["start"] = timestamp_match.group(1)
                current_caption["end"] = timestamp_match.group(2)
            
            # If the line is not empty, treat it as part of the caption text
            elif line and not timestamp_match:
                if current_caption["text"]:
                    current_caption["text"] += " " + line
                else:
                    current_caption["text"] = line
        
        # Append the last caption
        if current_caption["text"]:
            captions.append(current_caption)
    
    return captions


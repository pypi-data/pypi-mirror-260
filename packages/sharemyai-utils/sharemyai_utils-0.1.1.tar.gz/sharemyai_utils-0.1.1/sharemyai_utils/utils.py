import datetime
import io
import json
import os
import re
import torch
import torchaudio
from torchvision.io import write_video
from torchvision.transforms import ToTensor
from PIL import Image
from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
import cv2
import numpy as np
import os

def load_model_config(model_config_path=None):
    if model_config_path is None:
        model_config_path = os.path.join(os.getcwd(), "model.json")
    try:
        with open(model_config_path, "r") as file:
            model_config = json.load(file)
            default_params = model_config.get("params", {})
            plugin_name = model_config.get("name", "it broke")
    except FileNotFoundError:
        print(f"Warning: {model_config_path} not found. Using empty default parameters.")
        default_params = {}
        plugin_name = "it broke"
    return plugin_name, default_params


def check_for_saved_config(plugin_name, pipe_dict, default_params, load_pipe):
    model_dir = os.getenv("HF_HOME") or "./models" 
    filename = os.path.join(model_dir, f"{plugin_name}_server_config.json")
    try:
        with open(filename) as f:
            data = json.load(f)
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, 'w') as f:
            json.dump({}, f)
        data = {}

    if data.get("default_params"):
        default_params.update(data["default_params"])
    if data.get("pipeline"): # this will be the name 
        pipe_dict["name"] = data["pipeline"]
        pipe_dict["pipeline"] = load_pipe(data["pipeline"])
    if data.get("loras"):
        pipe_dict["loras"] = data["loras"]
    if data.get("adapter_weights"):
        pipe_dict["adapter_weights"] = data["adapter_weights"]
    if "loras" in pipe_dict and len(pipe_dict["loras"]) > 0 and "adapter_weights" in pipe_dict and len(pipe_dict["adapter_weights"]) > 0:
        # convert the weights to numbers
        pipe_dict["adapter_weights"] = [float(weight) for weight in pipe_dict["adapter_weights"]]
        for lora in pipe_dict["loras"]:
            pipe_dict["pipeline"].load_lora_weights(lora['url'], weight_name=lora['weight_name'], adapter_name=lora['adapter_name'])
        pipe_dict["pipeline"].set_adapters([lora['adapter_name'] for lora in pipe_dict['loras']], adapter_weights=pipe_dict["adapter_weights"])
        pipe_dict["pipeline"].fuse_lora(adapter_names=[lora['adapter_name'] for lora in pipe_dict['loras']])


def save_different_params(plugin_name, params):
    model_dir = os.getenv("HF_HOME", "./models")
    filename = os.path.join(model_dir, f"{plugin_name}_server_config.json")
    try:
        with open(filename, "r") as f:
            current_config = json.load(f)
        saved_params = current_config.get("default_params", {})
        different_params = [k for k, v in saved_params.items() if k != 'prompt' and str(params.get(k)) != str(v)]
        if different_params:
            print(f"Different params: {', '.join(different_params)}")
            print("Saving new params to server config")
            # Update only the different parameters to avoid overwriting with defaults
            for param in different_params:
                current_config["default_params"][param] = str(params[param]) if isinstance(params[param], bool) else params[param]
            with open(filename, "w") as f:
                json.dump(current_config, f, indent=4)
    except FileNotFoundError:
        with open(filename, "w") as f:
            json.dump({"default_params": params}, f, indent=4)


# takes in a pillow file and saves it to disk with proper formatting
def save_image(file, file_ext, prefix):
    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.{file_ext}"
    outpath = os.path.join(inference_directory, filename)
    outdir = os.path.dirname(outpath)
    
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    file.save(outpath, format='PNG')
    
    # Explicitly delete the image object if it's no longer needed
    del file
    return outpath

def custom_export_to_video(frames, out_path, fps=14):
    # Check the file extension
    file_ext = os.path.splitext(out_path)[1]
    if file_ext == '.gif':
        # Save frames as a GIF
        frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=1/fps)
    else:
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(out_path, fourcc, fps, (frames[0].size[1], frames[0].size[0]))
        for frame in frames:
            # Convert the image from BGR to RGB
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
            # Write the converted image
            video.write(frame)
        # Release the VideoWriter
        video.release()

def save_gif(frames, prefix, fps=24, quality=95, loop=1):
    imgs = frames #[Image.open(f) for f in sorted(frames)]
    if quality < 95:
        imgs = list(map(lambda x: x.resize((128, 128), Image.LANCZOS), imgs))
    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the prefix by removing special characters other than "_" and "-"
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.gif"
    outpath = os.path.join(inference_directory, filename) 
    outdir = os.path.dirname(outpath)
    duration_per_frame = 1000 // fps
    imgs[0].save(
        fp=outpath,
        format="GIF",
        append_images=imgs[1:],
        save_all=True,
        duration=duration_per_frame,
        loop=loop,
        quality=quality,
    )
    return outpath

def save_video(frames, prefix, fps=24, quality=95, audio_input=None):
    imgs = frames #[Image.open(f) for f in sorted(frames, key=lambda x: x.split("/")[-1])]
    if quality < 95:
        imgs = list(map(lambda x: x.resize((128, 128), Image.LANCZOS), imgs))

    img_tensors = [ToTensor()(img) for img in imgs]
    img_tensors = list(map(lambda x: x.unsqueeze(0), img_tensors))

    img_tensors = torch.cat(img_tensors)
    img_tensors = img_tensors * 255.0
    img_tensors = img_tensors.permute(0, 2, 3, 1)
    img_tensors = img_tensors.to(torch.uint8)

    inference_directory = os.getenv("INFERENCE_DIRECTORY", "./inference")
    datestr = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Clean the prefix by removing special characters other than "_" and "-"
    clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
    filename = f"{datestr}_{clean_prefix}.mp4"
    outpath = os.path.join(inference_directory, filename) 
    outdir = os.path.dirname(outpath)

    if audio_input is not None:
        audio_duration = len(img_tensors) / fps
        waveform, sr = torchaudio.load(audio_input)
        if waveform.shape[0] > 1:  # Check if audio is stereo
            waveform = torch.mean(waveform, dim=0, keepdim=True)  # Convert to mono
        num_frames = int(sr * audio_duration)
        waveform = waveform[:, :num_frames]  # Trim the waveform to the video duration
        audio_tensor = waveform.unsqueeze(0)

        write_video(
            outpath,
            video_array=img_tensors,
            fps=fps,
            audio_array=audio_tensor,
            audio_fps=sr,
            audio_codec="aac",
            video_codec="libx264",
        )
    else:
        write_video(
            outpath,
            video_array=img_tensors,
            fps=fps,
            video_codec="libx264",
        )

    return outpath

def create_app(name):
    app = Flask(name)
    CORS(app, resources={r"/*": {"origins": "*"}})  # This will enable CORS for all routes and all origins
    sock = Sock(app)

    print(f"cudnn version={torch.backends.cudnn.version()}")
    print(f"torch version={torch.__version__}")
    print(f"torch cuda version={torch.version.cuda}")

    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    return app, sock, device


# Helper method to create a safe file name
def create_safe_file_name(file_name):
    # Replace special characters in the file name to avoid OSError
    return re.sub(r'[\\/*?:"<>|]', "", file_name)

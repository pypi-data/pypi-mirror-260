import requests
import json
from typing import List
from typing import Dict, Any
from base64 import b64encode 

class ParrotAPI:
    """A Python wrapper for interacting with the Parrot API.

    Attributes:
        base_url (str): The base URL for the Parrot API.
        headers (dict): The headers to include credential. Will be updated after login.
    """
    
    def __init__(self, api_endpoint: str = "https://api.joinparrot.ai/v1") -> None:
        """Initialize the ParrotAPI with an API key.
        
        Args:
            api_key: A valid API key as a string.
        """
        self.base_url = api_endpoint

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Obtain Token via Basic Auth.
        
        Args:
            refresh_token: The refresh token as a string.
        
        Returns:
            A dictionary with the new token information.
        """
        url = f"{self.base_url}/user/login"
        # Authorization token: we need to base 64 encode it 
        # and then decode it to acsii as python 3 stores it as a byte string
        def basic_auth(username, password):
            token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
            return f'Basic {token}'

        #then connect
        headers = { 'Authorization' : basic_auth(username, password) }        
        response = requests.post(url, headers= headers)

        # obtain the token
        token = response.json()["data"]["access_token"]
        self.headers = {'Authorization' :  'Bearer ' + token}
        
        return response.json()

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh the API token using a refresh token.
        
        Args:
            refresh_token: The refresh token as a string.
        
        Returns:
            A dictionary with the new token information.
        """
        url = f"{self.base_url}/user/refresh_token"
        form = {"refresh_token": refresh_token}
        response = requests.post(url, data=form, headers=self.headers)
        return response.json()        

    def get_user_profile(self) -> Dict[str, Any]:
        """Retrieve the user's profile information.
        
        Returns:
            A dictionary containing the user's profile information.
        """
        url = f"{self.base_url}/user/me"
        response = requests.post(url, headers=self.headers)
        return response.json()

    def get_task_history(self) -> Dict[str, Any]:
        """Retrieve the user's task history.
        
        Returns:
            A dictionary containing the user's task history.
        """
        url = f"{self.base_url}/user/history"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_config(self, rotation: str = "square", steps: int = 50, negative_prompt: str = "", enhance_prompt: bool = False) -> Dict[str, Any]:
        """Helper function to create a configuration for the create_sdxl_task.
        
        Args:
            rotation: The orientation of the image ('square', 'horizontal', 'vertical').
            steps: The number of steps for the image generation process.
            negative_prompt: Aspects to avoid in the generated image.
        
        Returns:
            A configuration dictionary for the image task.
        """
        return {
            "rotation": rotation,
            "steps": steps,
            "negative_prompt": negative_prompt,
            "lora_weight_url": "",
            "enhance_prompt": enhance_prompt        
        }

    def create_sdxl_task(self, prompt: str, rotation: str = "square", steps: int = 50, negative_prompt: str = "", enhance_prompt: bool = False) -> Dict[str, Any]:
        """Create an SDXL-turbo image task with a prompt and configuration.
        
        Args:
            prompt: Description of the image to be generated.
            rotation: Image rotation preference.
            steps: Number of generation steps.
            negative_prompt: Negative aspects to avoid in the image.
        
        Returns:
            A dictionary with the task creation response.
        """
        config = self.create_config(rotation, steps, negative_prompt, enhance_prompt)
        url = f"{self.base_url}/ai/create_sdxl_task"
        payload = {"prompt": prompt, "config": config}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def create_sd_task(self, prompt: str, rotation: str = "square", steps: int = 50, negative_prompt: str = "", enhance_prompt: bool = False) -> Dict[str, Any]:
        """Create an SD1.5 image task with a prompt and configuration.
        
        Args:
            prompt: Description of the image to be generated.
            rotation: Image rotation preference.
            steps: Number of generation steps.
            negative_prompt: Negative aspects to avoid in the image.
        
        Returns:
            A dictionary with the task creation response.
        """
        config = self.create_config(rotation, steps, negative_prompt, enhance_prompt)
        url = f"{self.base_url}/ai/create_sd_task"
        payload = {"prompt": prompt, "config": config}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def create_lora_trainer_task(self, prompt: str, images: List[str]) -> Dict[str, Any]:
        """Create a LORA training task with the given prompt and images.

        Args:
            prompt: The text prompt for fine-tuning.
            images: A list of URLs pointing to images for fine-tuning.

        Returns:
            A dictionary containing the task ID and other response data.
        """
        url = f"{self.base_url}/ai/create_lora_trainner_task"

        files = [('files', image) for image in images]
        data = {'prompt': (None, prompt)}

        response = requests.post(url, files=files + list(data.items()), headers=self.headers)
        return response.json()
    
    def submit_feedback(self, task_id: str, rating: float, feedback: str) -> Dict[str, Any]:
        """Submit feedback for a completed task.

        Args:
            task_id: The unique identifier of the task.
            rating: A numeric rating value for the task outcome.
            feedback: Textual feedback about the task.

        Returns:
            A dictionary indicating the status of the feedback submission.
        """
        url = f"{self.base_url}/ai/feedback"
        payload = {"task_id": task_id, "rating": rating, "feedback": feedback}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def get_result_sd_task(self, task_id: str) -> Dict[str, Any]:
        """Retrieve the result of a previously submitted SD task.
        
        Args:
            task_id: The unique identifier of the SD task.
        
        Returns:
            A dictionary containing the result of the task.
        """
        url = f"{self.base_url}/ai/get_result_sd_task"
        payload = {"task_id": task_id}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def get_result_sdxl_task(self, task_id: str) -> Dict[str, Any]:
        """Retrieve the result of a previously submitted SDXL Turbo task.
        
        Args:
            task_id: The unique identifier of the SDXL Turbo task.
        
        Returns:
            A dictionary containing the result of the task.
        """
        url = f"{self.base_url}/ai/get_result_sdxl_task"
        payload = {"task_id": task_id}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()
    
    def get_result_lora_trainer_task(self, task_id: str) -> Dict[str, Any]:
        """Retrieve the result of a previously submitted LoRA Trainer task.
        
        Args:
            task_id: The unique identifier of the LoRA task.
        
        Returns:
            A dictionary containing the result of the task.
        """
        url = f"{self.base_url}/ai/get_result_lora_trainner_task"
        payload = {"task_id": task_id}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def get_all_models(self):
        """Get all models"""
        url = f"{self.base_url}/ai/models"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_txt2img(
        self,
        prompt: str,
        model: str = "sdxl-lightning",
        lora: str = "",
        width: int = 1024,
        height: int = 1024,
        steps: int = 8,
        seed: int = -1,
        negative_prompt: str = "",
        enhance_prompt: bool = False,
    ) -> Dict[str, Any]:
        """Create an text to image generation task with a prompt and configuration.

        Args:
            prompt (str): Description of the image to be generated.
            model (str): The type of model to be used. Default is "sdxl-lightning".
            lora (str): Optional parameter for LORA model.
            width (int): Width of the image. Default is 1024.
            height (int): Height of the image. Default is 1024.
            steps (int): Number of steps for image generation. Default is 8.
            seed (int): Random seed for image generation
            negative_prompt (str): Prompt for generating negative examples.
            enhance_prompt (bool): Whether to enhance the prompt or not. Default is False.

        Returns:
            A dictionary with the task creation response.
        """

        configs = dict(
            model=model, lora=lora, height=height, ưidth=width, steps=steps, negative_prompt=negative_prompt, seed=seed, enhance_prompt=enhance_prompt
        )
        url = f"{self.base_url}/ai/image_generation"
        payload = {"prompt": prompt, "configs": configs}
        response = requests.post(url, json=payload, headers=self.headers)

        return response.json()
    
    def result_txt2img(self, task_id: str):
        """Get result of text to image generation with task_id

        Args:
            task_id (str): The unique identifier of the text-to-image generation task.

        Returns:
            A dictionary with detail response.
        """
        url = f"{self.base_url}/ai/image_generation/{task_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_txt2vid(
        self,
        prompt: str,
        model: str = "modelscope-txt2vid",
        width: int = 512,
        height: int = 512,
        fps: int = 8,
        num_frames: int = 16,
        steps: int = 25,
        seed: int = -1,
        negative_prompt: str = "",
        enhance_prompt: bool = False,
    ) -> Dict[str, Any]:
        """Create an text to video generation task with a prompt and configuration.

        Args:
            prompt (str): Description of the video to be generated.
            model (str): The type of model to be used. Default is "modelscope-txt2vid"".
            width (int): Width of the image. Default is 512.
            height (int): Height of the image. Default is 512.
            fps (int): Number of frames per second.
            num_frames (int): Number of frames in the video.
            steps (int): Number of steps for video generation. Default is 8.
            seed (int): Random seed for video generation
            negative_prompt (str): Prompt for generating negative examples.
            enhance_prompt (bool): Whether to enhance the prompt or not. Default is False.

        Returns:
            A dictionary with the task creation response.
        """
        configs = dict(
            model=model, width=width, height=height, fps=fps, num_frames=num_frames, steps=steps, negative_prompt=negative_prompt, seed=seed, enhance_prompt=enhance_prompt
        )
        url = f"{self.base_url}/ai/video_generation"
        payload = {"prompt": prompt, "configs": configs}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def result_txt2vid(self, task_id: str):
        """Get result of text to video generation with task_id

        Args:
            task_id (str): Unique task ID of the text-to-video generation task.

        Returns:
            A dictionary with detail response.
        """
        url = f"{self.base_url}/ai/video_generation/{task_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()
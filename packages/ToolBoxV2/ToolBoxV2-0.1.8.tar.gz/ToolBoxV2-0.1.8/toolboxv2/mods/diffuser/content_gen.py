# cli_functions.py
# pip install git+https://github.com/huggingface/accelerate
import os

from diffusers import (StableDiffusionPipeline, AutoencoderTiny, AutoPipelineForText2Image, AutoPipelineForImage2Image, \
                       StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, DiffusionPipeline, LCMScheduler, \
                       AutoPipelineForInpainting, StableDiffusionControlNetPipeline, ControlNetModel,
                       AnimateDiffPipeline,
                       MotionAdapter, StableVideoDiffusionPipeline)
from diffusers.utils import load_image, make_image_grid, export_to_gif, export_to_video
import torch
import time
import cv2
import numpy as np
from PIL import Image

torch_dtype = torch.int16

grafic_provider = ["cpu", "gpu"][1]
performace_mode = ["high", "medium", "low", "mini"][1]

if performace_mode == "high":
    torch_dtype = torch.float64
if performace_mode == "medium":
    torch_dtype = torch.float16
if performace_mode == "low":
    torch_dtype = torch.int16
if performace_mode == "low":
    torch_dtype = torch.int8


class PipelineManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def to_pipline(self, pipe):

        if grafic_provider == "gpu":
            pipe.to("cuda")
        else:
            pipe.enable_model_cpu_offload()
        try:
            if performace_mode in ["low", "mini"]:
                pipe.unet.enable_forward_chunking()
            else:
                pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)
        except:
            pass

        return pipe

    def to_vpipline(self, pipe):

        if grafic_provider == "gpu":
            pipe.to("cuda")
        else:

            pipe.enable_vae_slicing()
            pipe.enable_model_cpu_offload()
        try:
            if performace_mode in ["low", "mini"]:
                pipe.unet.enable_forward_chunking()

            else:
                pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)
        except:
            pass

        return pipe

    def classic_generation(self, prompt, model="CompVis/stable-diffusion-v1-4",

                           NUM_INFERENCE_STEPS=25,
                           NUM_IMAGES_PER_PROMPT=4,
                           seed=2023):
        generator = torch.manual_seed(seed)
        if not hasattr(self, 'original'):
            self.original = self.to_pipline(StableDiffusionPipeline.from_pretrained(
                model, torch_dtype=torch_dtype, use_safetensors=True
            ))

        start = time.time_ns()
        images = self.original(
            prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            generator=generator,
            num_images_per_prompt=NUM_IMAGES_PER_PROMPT
        ).images
        end = time.time_ns()
        original_sd = f"{(end - start) / 1e6:.1f}"

        print(f"Execution time -- {original_sd} ms\n")
        return images

    def tiny_generation(self, prompt, model="nota-ai/bk-sdm-small", tiny="sayakpaul/taesd-diffusers",
                        NUM_INFERENCE_STEPS=25,
                        NUM_IMAGES_PER_PROMPT=4,
                        seed=2023):
        if not hasattr(self, 'distilled'):
            self.distilled = self.to_pipline(StableDiffusionPipeline.from_pretrained(
                model, torch_dtype=torch_dtype, use_safetensors=True,
            ))
            self.distilled.vae = self.to_pipline(AutoencoderTiny.from_pretrained(
                tiny, torch_dtype=torch_dtype, use_safetensors=True,
            ))
        generator = torch.manual_seed(seed)

        start = time.time_ns()
        images = self.distilled(
            prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            generator=generator,
            num_images_per_prompt=NUM_IMAGES_PER_PROMPT
        ).images
        end = time.time_ns()
        distilled_tiny_sd = f"{(end - start) / 1e6:.1f}"

        print(f"Execution time -- {distilled_tiny_sd} ms\n")
        return images

    def text_to_image_generation(self, prompt, num_inference_steps=1, guidance_scale=0.0):

        if not hasattr(self, 'pipeline_text2image'):
            self.pipeline_text2image = self.to_pipline(AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo", torch_dtype=torch.float16
            ))
        image = self.pipeline_text2image(prompt=prompt, guidance_scale=guidance_scale,
                                         num_inference_steps=num_inference_steps).images[0]
        return image

    def image_to_image_generation(self, prompt, init_image_url, strength=0.5,
                                  guidance_scale=0.0,
                                  num_inference_steps=2):
        init_image = load_image(init_image_url)
        init_image = init_image.resize((512, 512))

        if not hasattr(self, 'pipeline_text2image'):
            self.pipeline_text2image = self.to_pipline(AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo", torch_dtype=torch_dtype, variant="fp16"
            ))
        if not hasattr(self, 'pipeline_image2image'):
            self.pipeline_image2image = self.to_pipline(AutoPipelineForImage2Image.from_pipe(self.pipeline_text2image))

        image = self.pipeline_image2image(prompt, image=init_image,
                                          strength=strength,
                                          guidance_scale=guidance_scale,
                                          num_inference_steps=num_inference_steps).images[0]
        return make_image_grid([init_image, image], rows=1, cols=2)

    def xl_text_to_image_generation(self, prompt, model="stabilityai/stable-diffusion-xl-base-1.0"):
        if not hasattr(self, 'pipeline_xl'):
            self.pipeline_xl = self.to_pipline(StableDiffusionXLPipeline.from_pretrained(
                model, torch_dtype=torch_dtype, variant="fp16",
                use_safetensors=True,
                add_watermarker=False
            ))
        image = self.pipeline_xl(prompt=prompt).images[0]
        return image

    def xl_image_to_image_generation(self, prompt, init_image_url, strength=0.5,
                                     guidance_scale=0.0,
                                     num_inference_steps=2):
        init_image = load_image(init_image_url)
        init_image = init_image.resize((512, 512))
        if not hasattr(self, 'pipeline_image2image'):
            self.pipeline_image2image = self.to_pipline(AutoPipelineForImage2Image.from_pipe(self.pipeline_text2image))

        image = self.pipeline_image2image(prompt, image=init_image,
                                          strength=strength,
                                          guidance_scale=guidance_scale,
                                          num_inference_steps=num_inference_steps).images[0]
        return make_image_grid([init_image, image], rows=1, cols=2)

    def xl_base_generation(self, prompt):
        if not hasattr(self, 'pipeline_xl'):
            self.pipeline_xl = self.to_pipline(StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch_dtype, variant="fp16",
                use_safetensors=True,
                add_watermarker=False
            ))
        image = self.pipeline_xl(prompt=prompt).images[0]
        return image

    def xl_refiner_generation(self, prompt, init_image_url, strength=0.5,
                                     guidance_scale=0.0,
                                     num_inference_steps=2):
        if not hasattr(self, 'pipeline_xl_refiner'):
            self.pipeline_xl_refiner = self.to_pipline(StableDiffusionXLImg2ImgPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch_dtype, use_safetensors=True,
                variant="fp16", add_watermarker=False
            ))
        init_image = load_image(init_image_url)
        init_image = init_image.resize((512, 512))

        image = self.pipeline_xl_refiner(prompt, image=init_image,
                                          strength=strength,
                                          guidance_scale=guidance_scale,
                                          num_inference_steps=num_inference_steps).images[0]
        return make_image_grid([init_image, image], rows=1, cols=2)

    def inpainting_generation(self, prompt, init_image_url, mask_image_url):
        if not hasattr(self, 'pipeline_inpainting'):
            self.pipeline_inpainting = self.to_pipline(AutoPipelineForInpainting.from_pretrained(
                "runwayml/stable-diffusion-inpainting", torch_dtype=torch_dtype, variant="fp16"
            ))
        init_image = load_image(init_image_url)
        mask_image = load_image(mask_image_url)

        generator = torch.manual_seed(0)
        image = self.pipeline_inpainting(prompt=prompt, image=init_image, mask_image=mask_image,
                                         generator=generator, num_inference_steps=4, guidance_scale=4).images[0]
        return make_image_grid([init_image, mask_image, image], rows=1, cols=3)

    def controlnet_generation(self, prompt, input_image_url):

        if not hasattr(self, 'pipeline_controlnet'):
            self.pipeline_controlnet = self.to_pipline(StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                controlnet=ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch_dtype),
                torch_dtype=torch_dtype,
                safety_checker=None,
                variant="fp16"
            ))

        input_image = load_image(input_image_url)
        input_image = np.array(input_image)

        low_threshold = 100
        high_threshold = 200

        input_image = cv2.Canny(input_image, low_threshold, high_threshold)
        input_image = input_image[:, :, None]
        input_image = np.concatenate([input_image, input_image, input_image], axis=2)
        canny_image = Image.fromarray(input_image)

        generator = torch.manual_seed(0)
        image = self.pipeline_controlnet(prompt, image=canny_image, num_inference_steps=4,
                                         guidance_scale=1.5, controlnet_conditioning_scale=0.8,
                                         cross_attention_kwargs={"scale": 1}, generator=generator).images[0]
        return make_image_grid([canny_image, image], rows=1, cols=2)

    def diffusion_lora(self, prompt):

        if not hasattr(self, 'pipe_diffusion'):
            self.pipe_diffusion = self.to_pipline(DiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                variant="fp16",
                torch_dtype=torch_dtype
            ))
            self.pipe_diffusion.scheduler = LCMScheduler.from_config(self.pipe_diffusion.scheduler.config)
            self.pipe_diffusion.load_lora_weights("latent-consistency/lcm-lora-sdxl")

        generator = torch.manual_seed(42)
        return self.pipe_diffusion(
            prompt=prompt, num_inference_steps=4, generator=generator, guidance_scale=1.0
        ).images

    def animagine_lora(self, prompt):
        if not hasattr(self, 'pipe_animagine'):
            self.pipe_animagine = self.to_pipline(DiffusionPipeline.from_pretrained(
                "Linaqruf/animagine-xl",
                variant="fp16",
                torch_dtype=torch_dtype
            ))

            self.pipe_animagine.scheduler = LCMScheduler.from_config(self.pipe_animagine.scheduler.config)
            self.pipe_animagine.load_lora_weights("latent-consistency/lcm-lora-sdxl")
        generator = torch.manual_seed(0)
        return self.pipe_animagine(
            prompt=prompt, num_inference_steps=4, generator=generator, guidance_scale=1.0
        ).images

    def adreamshaper_lora(self, prompt, url):
        if not hasattr(self, 'pipe_dreamshaper'):
            self.pipe_dreamshaper = self.to_pipline(AutoPipelineForImage2Image.from_pretrained(
                "Lykon/dreamshaper-7",
                torch_dtype=torch_dtype,
                variant="fp16"
            ))

            self.pipe_dreamshaper.scheduler = LCMScheduler.from_config(self.pipe_dreamshaper.scheduler.config)
            self.pipe_dreamshaper.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")

        # prepare image
        init_image = load_image(url)

        # pass prompt and image to pipeline
        generator = torch.manual_seed(0)
        return self.pipe_dreamshaper(
            prompt,
            image=init_image,
            num_inference_steps=4,
            guidance_scale=1,
            strength=0.6,
            generator=generator
        ).images

    def classic_video_generation(self, prompt,
                                 negative_prompt=None,
                                 adapter_model="wangfuyun/AnimateLCM",
                                 animate_model="emilianJR/epiCRealism",
                                 NUM_INFERENCE_STEPS=6,
                                 num_frames=16,
                                 guidance_scale=2.0,
                                 seed=2023,
                                 to_gif=True,
                                 export_fps=12,
                                 plath="output"):

        if negative_prompt is None:
            negative_prompt = "bad quality, worse quality, low resolution"

        if not hasattr(self, 'Animate_pipe'):
            adapter = MotionAdapter.from_pretrained(adapter_model, torch_dtype=torch_dtype)
            self.Animate_pipe = AnimateDiffPipeline.from_pretrained(animate_model, motion_adapter=adapter,
                                                                    torch_dtype=torch_dtype)
            self.Animate_pipe.scheduler = LCMScheduler.from_config(self.Animate_pipe.scheduler.config,
                                                                   beta_schedule="linear")
            self.Animate_pipe = self.to_vpipline(self.Animate_pipe)
            # self.Animate_pipe.set_adapters(["lcm-lora"], [0.8])

        start = time.time_ns()
        generator = torch.manual_seed(seed)
        output = self.Animate_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_frames=num_frames,
            guidance_scale=guidance_scale,
            num_inference_steps=NUM_INFERENCE_STEPS,
            generator=generator,
        )
        frames = output.frames[0]

        original_sd = f"{(time.time_ns() - start) / 1e6:.1f}"
        print(f"Execution time -- {original_sd} ms\n")
        if to_gif:
            return export_to_gif(frames, plath + '.gif')
        return export_to_video(frames, plath + ".mp4", fps=export_fps)

    def classic_image_animation(self, url,
                                decode_chunk_size=8,
                                motion_bucket_id=180,
                                noise_aug_strength=0.1,
                                image_size=(1024, 576),
                                seed=2023,
                                to_gif=True,
                                export_fps=12,
                                model="stabilityai/stable-video-diffusion-img2vid-xt",
                                plath="output"):

        if not hasattr(self, 'image_animatio_pipe'):
            self.image_animatio_pipe = self.to_vpipline(StableVideoDiffusionPipeline.from_pretrained(
                model, torch_dtype=torch.float16, variant="fp16"
            ))

        start = time.time_ns()

        image = load_image(url)
        image = image.resize(image_size)

        generator = torch.manual_seed(seed)
        frames = self.image_animatio_pipe(image, decode_chunk_size=decode_chunk_size,
                                          generator=generator,
                                          motion_bucket_id=motion_bucket_id,
                                          noise_aug_strength=noise_aug_strength).frames[0]
        original_sd = f"{(time.time_ns() - start) / 1e6:.1f}"
        print(f"Execution time -- {original_sd} ms\n")
        if to_gif:
            return export_to_gif(frames, plath + '.gif')
        return export_to_video(frames, plath + ".mp4", fps=export_fps)

    def text_to_animation(self, prompt,
                          num_inference_steps=5,
                          guidance_scale=1.25,
                          cross_attention_kwargs=None,
                          num_frames=24,
                          seed=2023,
                          to_gif=True,
                          export_fps=7,
                          plath="output"):

        if cross_attention_kwargs is None:
            cross_attention_kwargs = {"scale": 1}
        if not hasattr(self, 'gif_pipe'):
            adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5", token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
            self.gif_pipe = self.to_vpipline(AnimateDiffPipeline.from_pretrained(
                "frankjoshua/toonyou_beta6",
                motion_adapter=adapter,
            ))

            # set scheduler
            self.gif_pipe.scheduler = LCMScheduler.from_config(self.gif_pipe.scheduler.config)

            # load LCM-LoRA
            self.gif_pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5", adapter_name="lcm")
            self.gif_pipe.load_lora_weights("guoyww/animatediff-motion-lora-zoom-in",
                                            weight_name="diffusion_pytorch_model.safetensors",
                                            adapter_name="motion-lora")

            self.gif_pipe.set_adapters(["lcm", "motion-lora"], adapter_weights=[0.55, 1.2])

        start = time.time_ns()

        generator = torch.manual_seed(seed)

        frames = self.gif_pipe(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            cross_attention_kwargs=cross_attention_kwargs,
            num_frames=num_frames,
            generator=generator
        ).frames[0]

        export_to_video(frames, "generated.mp4", fps=export_fps)
        original_sd = f"{(time.time_ns() - start) / 1e6:.1f}"
        print(f"Execution time -- {original_sd} ms\n")
        if to_gif:
            return export_to_gif(frames, plath + '.gif')
        return export_to_video(frames, plath + ".mp4", fps=export_fps)


def display_and_save_image(image, save_path=None):
    try:
        image.show()
        return
    except Exception as e:
        print("Error", e)
        print("Image ", type(image), image)
        img = Image.fromarray(image)
        img.show()
    if save_path is not None:
        img.save(save_path)



def prmitivrunner():
    manager = PipelineManager()

    while True:
        print("1. Classic Generation")
        print("2. Tiny Generation")
        print("3. Text-to-Image Generation")
        print("4. Image-to-Image Generation")
        print("5. XL Text-to-Image Generation")
        print("6. XL Image-to-Image Generation")
        print("7. XL Base Generation")
        print("8. XL Refiner Generation")
        print("9. Inpainting Generation")
        print("10. Controlnet Generation")
        print("11. Diffusion Lora")
        print("12. Animagine Lora")
        print("13. Adreamshaper Lora")
        print("14. Classic Video Generation")
        print("15. Classic Image Animation")
        print("16. Text-to-Animation")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            prompt = input("Enter the prompt: ")
            images = manager.classic_generation(prompt)
            for image in images:
                display_and_save_image(image)

        elif choice == "2":
            prompt = input("Enter the prompt: ")
            images = manager.tiny_generation(prompt)
            for image in images:
                display_and_save_image(image)

        elif choice == "3":
            prompt = input("Enter the prompt: ")
            num_inference_steps = int(input("Enter the num_inference_steps 1: "))
            guidance_scale = float(input("Enter the guidance_scale 0.0: "))
            image = manager.text_to_image_generation(prompt,
                                                     num_inference_steps=num_inference_steps
                                                     , guidance_scale=guidance_scale, )
            display_and_save_image(image)

        elif choice == "4":
            prompt = input("Enter the prompt: ")
            init_image_url = input("Enter the URL of the initial image: ")

            num_inference_steps = int(input("Enter the num_inference_steps 2: "))
            guidance_scale = float(input("Enter the guidance_scale 0.0: "))
            strength = float(input("Enter the strength 0.5: "))

            image = manager.image_to_image_generation(prompt, init_image_url,
                                                      strength=strength,
                                                      num_inference_steps=num_inference_steps
                                                      , guidance_scale=guidance_scale)
            display_and_save_image(image)

        elif choice == "5":
            prompt = input("Enter the prompt: ")
            image = manager.xl_text_to_image_generation(prompt)
            display_and_save_image(image)

        elif choice == "6":
            prompt = input("Enter the prompt: ")
            init_image_url = input("Enter the URL of the initial image: ")
            num_inference_steps = int(input("Enter the num_inference_steps 2: "))
            guidance_scale = float(input("Enter the guidance_scale 0.0: "))
            strength = float(input("Enter the strength 0.5: "))
            image = manager.xl_image_to_image_generation(prompt, init_image_url,
                                                         strength=strength,
                                                         num_inference_steps=num_inference_steps
                                                         , guidance_scale=guidance_scale)
            display_and_save_image(image)

        elif choice == "7":
            prompt = input("Enter the prompt: ")
            image = manager.xl_base_generation(prompt)
            display_and_save_image(image)

        elif choice == "8":
            prompt = input("Enter the prompt: ")
            init_image_url = input("Enter the URL of the initial image: ")

            num_inference_steps = int(input("Enter the num_inference_steps 2: "))
            guidance_scale = float(input("Enter the guidance_scale 0.0: "))
            strength = float(input("Enter the strength 0.5: "))
            image = manager.xl_refiner_generation(prompt, init_image_url,
                                                         strength=strength,
                                                         num_inference_steps=num_inference_steps
                                                         , guidance_scale=guidance_scale)
            display_and_save_image(image)

        elif choice == "9":
            prompt = input("Enter the prompt: ")
            init_image_url = input("Enter the URL of the initial image: ")
            mask_image_url = input("Enter the URL of the mask image: ")
            image = manager.inpainting_generation(prompt, init_image_url, mask_image_url)
            display_and_save_image(image)

        elif choice == "10":
            prompt = input("Enter the prompt: ")
            input_image_url = input("Enter the URL of the input image: ")
            image = manager.controlnet_generation(prompt, input_image_url)
            display_and_save_image(image)

        elif choice == "11":
            prompt = input("Enter the prompt: ")
            images = manager.diffusion_lora(prompt)
            for image in images:
                display_and_save_image(image)

        elif choice == "12":
            prompt = input("Enter the prompt: ")
            images = manager.animagine_lora(prompt)
            for image in images:
                display_and_save_image(image)

        elif choice == "13":
            prompt = input("Enter the prompt: ")
            url = input("Enter the URL of the image: ")
            images = manager.adreamshaper_lora(prompt, url)
            for image in images:
                display_and_save_image(image)

        elif choice == "14":
            prompt = input("Enter the prompt: ")
            negative_prompt = input("Enter the negative prompt: ")
            num_frames = int(input("Enter the number of frames: "))
            to_gif = input("Export to GIF? (y/n): ").lower() == "y"
            export_fps = int(input("Enter the export FPS: "))
            plath = input("Enter the path to save the output: ")
            manager.classic_video_generation(prompt,
                                             negative_prompt=negative_prompt,
                                             num_frames=num_frames,
                                             to_gif=to_gif,
                                             export_fps=export_fps,
                                             plath=plath)

        elif choice == "15":
            url = input("Enter the URL of the image: ")
            decode_chunk_size = int(input("Enter the decode chunk size 8: "))
            motion_bucket_id = int(input("Enter the motion bucket ID 180: "))
            noise_aug_strength = float(input("Enter the noise augmentation strength 0.1: "))
            image_size = tuple(map(int, input("Enter the image size (width height) (1024 576)): ").split()))
            to_gif = input("Export to GIF? (y/n): ").lower() == "y"
            export_fps = int(input("Enter the export FPS 7/12/16: "))
            plath = input("Enter the path to save the : ")
            manager.classic_image_animation(url,
                                            decode_chunk_size=decode_chunk_size,
                                            motion_bucket_id=motion_bucket_id,
                                            noise_aug_strength=noise_aug_strength,
                                            image_size=image_size,
                                            to_gif=to_gif,
                                            export_fps=export_fps,
                                            plath=plath)

        elif choice == "16":
            prompt = input("Enter the prompt: ")
            num_inference_steps = int(input("Enter the number of inference steps 5: "))
            guidance_scale = float(input("Enter the guidance scale: 1.25"))
            num_frames = int(input("Enter the number of frames: 24"))
            seed = int(input("Enter a seed: 42"))
            to_gif = input("Export to GIF? (y/n): ").lower() == "y"
            export_fps = int(input("Enter the export FPS 7/12/16: "))
            plath = input("Enter the path to save the output: ")
            manager.text_to_animation(prompt,
                                      num_inference_steps=num_inference_steps,
                                      guidance_scale=guidance_scale,
                                      num_frames=num_frames,
                                      seed=seed,
                                      to_gif=to_gif,
                                      export_fps=export_fps,
                                      plath=plath)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    #prmitivrunner()
    # pass
# Usage example:
    manager = PipelineManager()
    # tiny_generation 32 gib
    manager.text_to_animation("cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, "
                                     "Pixar, Disney, 8k")
#  manager.tiny_generation("a golden vase with different flowers")
# manager.text_to_image_generation("A cinematic shot of a baby racoon wearing an intricate italian priest robe.")
# manager.image_to_image_generation(
#     "cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, Pixar, Disney, 8k",
#     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/cat.png")
# manager.xl_text_to_image_generation("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k")
# manager.xl_image_to_image_generation("a dog catching a frisbee in the jungle",
#                                      "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/sdxl-text2img.png")
# manager.xl_base_generation("Astronaut in a jungle, cold color palette, muted colors, detailed, 8k")
# manager.xl_refiner_generation("a dog catching a frisbee in the jungle",
#                               "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/sdxl-text2img.png")
# manager.inpainting_generation(
#     "concept art digital painting of an elven castle, inspired by lord of the rings, highly detailed, 8k",
#     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/inpaint.png",
#     "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/inpaint_mask.png")
# manager.controlnet_generation("Self-portrait oil painting, a beautiful cyborg with golden hair, 8k",
#                               "https://hf.co/datasets/huggingface/documentation-images/resolve/main/diffusers/input_image_vermeer.png")

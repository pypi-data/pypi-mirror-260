import streamlit as st
from content_gen import PipelineManager
# from toolboxv2.utils.toolbox import ProxyApp


def main():
    manager = PipelineManager()

    st.sidebar.title("Generation Tasks")
    task = st.sidebar.selectbox("Select a task", ["Classic Generation", "Tiny Generation", "Text-to-Image Generation",
                                                  "Image-to-Image Generation", "XL Text-to-Image Generation",
                                                  "XL Image-to-Image Generation", "XL Base Generation",
                                                  "XL Refiner Generation", "Inpainting Generation",
                                                  "Controlnet Generation", "Diffusion Lora", "Animagine Lora",
                                                  "Adreamshaper Lora", "Classic Video Generation",
                                                  "Classic Image Animation", "Text-to-Animation"])

    st.text(task)

    prompt = st.text_input("Enter the prompt")

    if task == "Classic Generation":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                images = manager.classic_generation(prompt)
            for image in images:
                st.image(image)

    elif task == "Tiny Generation":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                images = manager.tiny_generation(prompt)
            for image in images:
                st.image(image)

    elif task == "Text-to-Image Generation":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.text_to_image_generation(prompt)
            st.image(image)

    elif task == "Image-to-Image Generation":
        init_image_url = st.text_input("Enter the URL of the initial image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.image_to_image_generation(prompt, init_image_url)
            st.image(image)

    elif task == "XL Text-to-Image Generation":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.xl_text_to_image_generation(prompt)
            st.image(image)

    elif task == "XL Image-to-Image Generation":
        init_image_url = st.text_input("Enter the URL of the initial image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.xl_image_to_image_generation(prompt, init_image_url)
            st.image(image)

    elif task == "XL Base Generation":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.xl_base_generation(prompt)
            st.image(image)

    elif task == "XL Refiner Generation":
        init_image_url = st.text_input("Enter the URL of the initial image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.xl_refiner_generation(prompt, init_image_url)
            st.image(image)

    elif task == "Inpainting Generation":
        init_image_url = st.text_input("Enter the URL of the initial image")
        mask_image_url = st.text_input("Enter the URL of the mask image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.inpainting_generation(prompt, init_image_url, mask_image_url)
            st.image(image)

    elif task == "Controlnet Generation":
        input_image_url = st.text_input("Enter the URL of the input image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                image = manager.controlnet_generation(prompt, input_image_url)
            st.image(image)

    elif task == "Diffusion Lora":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                images = manager.diffusion_lora(prompt)
            for image in images:
                st.image(image)

    elif task == "Animagine Lora":
        if st.button("Generate"):
            with st.spinner('Generating...'):
                images = manager.animagine_lora(prompt)
            for image in images:
                st.image(image)

    elif task == "Adreamshaper Lora":
        url = st.text_input("Enter the URL of the image")
        if st.button("Generate"):
            with st.spinner('Generating...'):
                images = manager.adreamshaper_lora(prompt, url)
            for image in images:
                st.image(image)

    elif task == "Classic Video Generation":
        negative_prompt = st.text_input("Enter the negative prompt")
        adapter_model = st.text_input("Enter the adapter model")
        animate_model = st.text_input("Enter the animate model")
        num_frames = st.number_input("Enter the number of frames", value=1)
        to_gif = st.checkbox("Export to GIF")
        export_fps = st.number_input("Enter the export FPS", value=1)
        plath = st.text_input("Enter the path to save the output")
        if st.button("Generate Video"):
            with st.spinner('Generating Video...'):
                manager.classic_video_generation(prompt, negative_prompt, adapter_model, animate_model,
                                                 num_frames, to_gif, export_fps, plath)
        if st.button("Show"):
            with open(plath, "r") as video_file:
                st.video(video_file)

    elif task == "Classic Image Animation":
        url = st.text_input("Enter the URL of the image")
        decode_chunk_size = st.number_input("Enter the decode chunk size", value=1)
        motion_bucket_id = st.number_input("Enter the motion bucket ID", value=1)
        noise_aug_strength = st.number_input("Enter the noise augmentation strength", value=0.0)
        image_size = st.text_input("Enter the image size (width height)")
        to_gif = st.checkbox("Export to GIF")
        export_fps = st.number_input("Enter the export FPS", value=1)
        model = st.text_input("Enter the model")
        plath = st.text_input("Enter the path to save the output")
        if st.button("Generate Video"):
            with st.spinner('Generating Video...'):
                manager.classic_image_animation(url, decode_chunk_size, motion_bucket_id, noise_aug_strength,
                                                image_size, to_gif, export_fps, model, plath)
        if st.button("Show"):
            with open(plath, "r") as video_file:
                st.video(video_file)

    elif task == "Text-to-Animation":
        num_inference_steps = st.number_input("Enter the number of inference steps", value=1)
        guidance_scale = st.number_input("Enter the guidance scale", value=0.0)
        num_frames = st.number_input("Enter the number of frames", value=1)
        seed = st.number_input("Enter the seed", value=1)
        to_gif = st.checkbox("Export to GIF")
        export_fps = st.number_input("Enter the export FPS", value=1)
        plath = st.text_input("Enter the path to save the output")
        if st.button("Generate Video"):
            with st.spinner('Generating Video...'):
                manager.text_to_animation(prompt, num_inference_steps, guidance_scale, num_frames, seed,
                                          to_gif, export_fps, plath)
        if st.button("Show"):
            with open(plath, "r") as video_file:
                st.video(video_file)


if __name__ == "__main__":
    main()

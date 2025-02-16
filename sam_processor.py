import cv2
import numpy as np
import torch
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from PIL import Image

# Load SAM model
sam_checkpoint = "sam_vit_b_01ec64.pth"  # Path to SAM checkpoint
print(torch.cuda.is_available())
device = "cuda"
model_type = "vit_b"  # Model type (vit_b or vit_l)

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device)

# Create the mask generator
mask_generator = SamAutomaticMaskGenerator(sam, points_per_batch=16)




def process_image_with_sam(pil_image ):
    # Resize the image to a smaller resolution
    pil_image = pil_image.resize((pil_image.width // 2, pil_image.height // 2))
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    print("Image Resizing done")

    # Generate masks using SAM
    masks = mask_generator.generate(image)
    pixel_area = 0.2 * 0.2  # Adjust as resolution is halved
    print("Image mask generation done")

    total_area = sum(np.sum(mask["segmentation"]) * pixel_area for mask in masks)
    return {"masks": masks, "total_area": total_area}


# def process_image_with_sam(pil_image):
#     # Resize the image to a smaller resolution
#     real_world_scale =10
#     pil_image = pil_image.resize((pil_image.width // 2, pil_image.height // 2))
#     image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
#     print("Image Resizing done")

#     # Generate masks using SAM
#     masks = mask_generator.generate(image)
#         # Calculate pixel area using the real-world scale
#     pixel_area = real_world_scale ** 2  # Area of one pixel in square meters

#     # Calculate total area covered by the masks
#     total_area = sum(np.sum(mask["segmentation"]) * pixel_area for mask in masks)

#     total_area = int(total_area.item()) if isinstance(total_area, np.integer) else int(total_area)
    
#     return {"masks": masks, "total_area": total_area}
# ANPRS (Automatic Number Plate Recognition System)

This project served as the B.Tech project of four Electrical Engineering students in 2022.

## Usage

1. Install Package (Requires python 3.x)
   ```
   pip install anprs
   ```
2. Sample Usage
   ```
    from anprs.anprs import LPR, OCR

    lpr = LPR()
    ocr = OCR()

    image_path = 'path/to/your/image'

    lpr_res = lpr.perform_lpr(image_path)

    license_plate_number = ""

    if lpr_res:
        license_plate_number = ocr.get_results()
    else:
        print('License plate not detected')

    print(lpr_res, license_plate_number)
   ```

## Research Paper

The implementation in this repository corresponds to the following research paper:

**Title:** Deep Learning-based approach for Indian License Plate Recognition using Optical Character Recognition

**Authors:** 
- Aditya Upadhye
- Atharvraj Patil
- Jayesh Ingale
- Sakshi Jaiswal
- Suhas Kakade
- Abhishek Bhatt
  
**Link:** https://ieeexplore.ieee.org/abstract/document/10183391


## Build Project

1. Setup Virtual Env

```
# create virtual env
python -m venv local_env

# use this to activate the environment
source local_env/Scripts/activate

# install dependencies
pip install -r requirements.txt
```

2. Create Media Folder in root directory
3. Add your image of a vehicle and rename it to photo.jpg
The Infiray P2 Pro is equipped with a radiometric sensor. This type of sensor allows the device to measure and record the temperature of objects within its field of view. In thermal imaging cameras like the Infiray P2 Pro, radiometric sensors are crucial for applications that require precise temperature measurements, such as in industrial inspections, electrical inspections, and building diagnostics. The radiometric sensor enables the camera to capture not just thermal images but also to provide temperature data for each pixel in the image. This feature enhances the utility of the device in various professional settings where accurate temperature readings are essential.

To look at individual pixel values in an image captured by a device like the Infiray P2 Pro, which has a radiometric sensor, you would typically need to use specialized software provided by the manufacturer or compatible third-party software. Here's a general process for examining pixel values:

1. **Capture and Save the Image**: Use the Infiray P2 Pro to capture the thermal image. Ensure the image is saved in a format that retains the radiometric data. This is often a proprietary format specific to the manufacturer.
    
2. **Transfer the Image to a Computer**: Connect the device to a computer or use a memory card to transfer the image files.
    
3. **Use Thermal Imaging Software**: Open the image in thermal imaging analysis software. Infiray likely provides its own software for this purpose, or you might be able to use compatible third-party software.
    
4. **Analyze the Image**: The software should allow you to hover over or click on individual pixels to see their temperature values. Some programs also allow you to analyze regions, set temperature thresholds, and see histograms of temperature distribution.
    
5. **Export Data**: If you need to process the data further, some software allows you to export the temperature data of each pixel, often in formats like CSV.
    

Remember, the resolution of your thermal image and the accuracy of the temperature readings will depend on the specifications of your Infiray P2 Pro's sensor and lens. The user manual or the manufacturer's website might have more detailed instructions specific to your model.


There are several open-source software options available for analyzing radiometric thermal images:

1. **IRimage**: This software is designed to increase throughput, accuracy, and reproducibility of results obtained from thermal images, especially those from affordable, consumer-oriented cameras. It enables the extraction of raw data from thermal images and the calculation of temperature values​ ([NCBI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9138121/#:~:text=IRimage%20was%20developed%20with%20the,images%20and%20calculate%20temperature))​.
    
2. **Thermimage**: Thermimage is a collection of functions that assist in converting extracted raw data from infrared thermal images into estimated temperatures using standard equations in thermography. This software provides an open-source tool for infrared thermographic analysis​ ([GitHub](https://github.com/gtatters/Thermimage#:~:text=Thermimage%3A%20Thermal%20Image%20Analysis,assisting%20with%20infrared%20thermographic%20analysis))​.
    
3. **IRimage-UAV**: This is an alternative version of IRimage, specifically adapted to process images from thermal cameras used in DJI drones. It shares the open-source nature of IRimage, allowing users to understand and modify the algorithms used to obtain temperature values​ ([GitHub](https://github.com/gpereyrairujo/IRimage#:~:text=IRimage%20is%20open%20source%2C%20in,cameras%20used%20in%20DJI%20drones))​.
    
4. **ThermImageJ**: Part of the ImageJ platform, ThermImageJ offers a collection of functions and macros for the import and conversion of thermal image files. It assists in extracting raw data from infrared thermal images and converting these to temperatures using standard equations in thermography​ ([GitHub](https://github.com/gtatters/ThermImageJ#:~:text=ThermImageJ%20is%20a%20collection%20of,using%20standard%20equations%20in%20thermography))​.
    
5. **FireCAM**: Although primarily a timelapse camera, FireCAM's associated software can handle both visual and radiometric thermal images. It records thermal images as raw radiometric data (temperature) in json-structured files, which can then be analyzed later​ ([GitHub](https://github.com/danjulio/firecam#:~:text=FireCAM%20is%20a%20timelapse%20camera,a%20touch%20LCD%20control))​.
    

Each of these tools offers unique features and capabilities, making them suitable for different types of analysis and applications in the field of thermal imaging. You would need to evaluate each based on your specific requirements for analyzing the pixel values in radiometric images.


When you read each pixel value of a radiometric thermal image, the data typically appears as numerical values representing the temperature at each pixel. This data is often in a matrix or grid format, corresponding to the layout of the pixels in the image. Here's a general idea of what the data might look like:

1. **Matrix Format**: The data can be represented as a two-dimensional array or matrix, where each entry in the array corresponds to a pixel in the image. For example, if the image is 320x240 pixels, you would have a 320x240 matrix.
    
2. **Temperature Values**: Each entry in this matrix represents the temperature at that particular pixel. The values are usually in a specific temperature unit, like Celsius or Kelvin.
    
3. **Numeric Representation**: These temperature values are typically represented as floating-point numbers. For instance, a value might read `23.4` or `310.15`, indicating the temperature at that pixel.
    
4. **Example of a Small Section**: For a very small 3x3 section of a larger image, the data might look something like this:

Each number represents the temperature at that pixel location.
    
2. **Metadata**: Along with the temperature values, there may also be metadata, such as the time the image was captured, the camera settings, the scale of temperature values, etc.
    
3. **Visualization**: When visualized, these values correspond to different colors on a thermal image, with each color representing a temperature range.
    
4. **File Formats**: The specific format of this data depends on how the image is saved and exported from the thermal imaging software. Common formats include CSV, JSON, or proprietary formats that require specific software to read.
    
5. **Post-Processing**: For further analysis, this data can often be exported and processed using various software tools, where you can apply statistical analysis, create heatmaps, or integrate the data into other systems for further interpretation.

We can use [[c++]] as well

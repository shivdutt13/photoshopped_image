# photoshopped_image
Python code to determine whether an image is photoshopped or not

**Introduction:**
1. In this python script, I use error level analysis (ELA) to determine whether an image is photoshopped or not. 
2. I researched the topic of how to determine whether the image is photoshopped, and decided to use the technique of error level analysis.
3. I found this sample script to work off of: https://gist.github.com/cirocosta/33c758ad77e6e6531392 - although I used this as a starting point, my script has many major differences and uses a different approach. 
4. I ran my script on several photoshopped and non-photoshopped images, and got the expected results.
5. I am writing the JSON payload to a file so that the rest of the output can be seen easily (i.e. not printing it out).
6. Please note that my script also gives a confidence interval/rating on whether an image is photoshopped or not - it doesn't just say yes/no.
7. Usage is: python error_level_analysis_v3.py --dir <directory that contains image> --fname <image_name>

**Sample Outputs:**
8. Sample output (for photoshopped image): 
[shiv@chef:~/python_scripts]$ python error_level_analysis_v3.py --dir "/home/shiv/" --fname "zane-lee-LvVw6wRmGAM-unsplash.jpg"
In the main function
Parsing the arguments
Performing ELA on image /home/shiv//zane-lee-LvVw6wRmGAM-unsplash.jpg

In the ELA function
org_fname is: /home/shiv/zane-lee-LvVw6wRmGAM-unsplash.jpg
tmp_fname is: /home/shiv/generated/zane-lee-LvVw6wRmGAM-unsplash.tmp_ela.jpg
ela_fname is: /home/shiv/generated/zane-lee-LvVw6wRmGAM-unsplash.ela.png

Opening the image
Opening the tmp image
ela_im is: <PIL.Image.Image image mode=RGB size=4016x6016 at 0x7FDFAF5B20D0>
extrema is: ((0, 21), (0, 12), (0, 35))
max_diff is: 35

The max_diff is: 35
The image is almost certainly photoshopped (95% confidence)
Check the ELA image at: /home/shiv//generated

Writing the JSON payload of the original image to file jayson_payload.txt
[shiv@chef:~/python_scripts]$


9. Sample output (for non-photoshopped image):
[shiv@chef:~/python_scripts]$ python error_level_analysis_v3.py --dir "/home/shiv/" --fname "Nahant_Beach.jpeg"
In the main function
Parsing the arguments
Performing ELA on image /home/shiv//Nahant_Beach.jpeg

In the ELA function
org_fname is: /home/shiv/Nahant_Beach.jpeg
tmp_fname is: /home/shiv/generated/Nahant_Beach.tmp_ela.jpg
ela_fname is: /home/shiv/generated/Nahant_Beach.ela.png

Opening the image
Opening the tmp image
ela_im is: <PIL.Image.Image image mode=RGB size=614x619 at 0x7F706A5DE0D0>
extrema is: ((0, 13), (0, 13), (0, 13))
max_diff is: 13

The max_diff is: 13
The image is more likely not photoshopped
Check the ELA image at: /home/shiv//generated

Writing the JSON payload of the original image to file jayson_payload.txt
[shiv@chef:~/python_scripts]$


**Additional Details:**

10. If I had additional days to work on this problem, what I would do: 
-- I would run the script over many more (thousands or more) of photoshopped and non-photoshopped images to get more strict/accurate values for the max_diff thresholds and more precise confidence intervals
-- I would include functions that use other techniques, such as the average color composition 
(see for exmaple: https://www.reddit.com/r/computervision/comments/5ivbI would cd/is_there_a_way_to_tell_if_an_image_has_been/)
-- I would check the metadata in the file to see if it gives any indication of manipulation using photoshop 
-- I would check areas of the image that are likely to have not been manipulated correctly (such as shadows, which I could find by looking at darker spots)

11. The solution should scale without much issue. 
If we have many files to analyze (say millions or more), then we would likely have to use some sort of multi-threading. 

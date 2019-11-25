import skew_detect 
import deskew

sd = skew_detect.SkewDetect(
	input_file='img_0.jpg',
	batch_path='optional_batch_processing_path',
	output_file='optional_text_file_output_path',
	display_output='Yes/No')
sd.run()

d = deskew.Deskew(
	input_file='img_0.jpg',
	display_image='preview the image on screen',
	output_file='path_for_deskewed_image',
	r_angle=0)
d.run()

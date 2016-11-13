def function_visual_rec(test_url):
	visual_recognition = VisualRecognitionV3('2016-05-20', api_key='d6559600e73999315b6fa8bcf9ab9b6f18fb217f')

	result = json.dumps(visual_recognition.classify(images_url=test_url), indent=2)

	parsed = json.loads(result)

	f = open('results.txt','w')
	f.write(result)
	f.close()
	beach = 0
	mountain = 0
	city = 0	
	var1 = parsed['images'][0]['classifiers'][0]['classes']
	for i in range(len(var1)):
		if parsed['images'][0]['classifiers'][0]['classes'][i]['class'] == 'beach':
			if parsed['images'][0]['classifiers'][0]['classes'][i]['score'] > 0.5:
				beach = 1
# extend here
	for i in range(len(var1)):
		if parsed['images'][0]['classifiers'][0]['classes'][i]['class'] == 'mountain':
			if parsed['images'][0]['classifiers'][0]['classes'][i]['score'] > 0.5:
				mountain = 1

	for i in range(len(var1)):
		if parsed['images'][0]['classifiers'][0]['classes'][i]['class'] == 'city':
			if parsed['images'][0]['classifiers'][0]['classes'][i]['score'] > 0.5:
				city = 1
	output = [beach,mountain,city]
	return output

import json
#from os.path import join, dirname
#from os import environ
from watson_developer_cloud import VisualRecognitionV3

if __name__ == '__main__':
	test_url = [];
	test_url.append('https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Skyscrapers_of_Shinjuku_2009_January_(revised).jpg/900px-Skyscrapers_of_Shinjuku_2009_January_(revised).jpg')
	test_url.append('http://images.mapsofindia.com/my-india/marina-beach-chennai.jpg')
	test_url.append('http://www.trawell.in/admin/images/upload/705431925Merina_Beach_Main.jpg')
	test_url.append('http://www.indialine.com/travel/images/colva-beach.jpg')
	test_url.append('http://images2.mygola.com/juhu-beach_5350710_m.jpg')
	test_url.append('http://imgc.allpostersimages.com/images/P-473-488-90/81/8132/WKWE300Z/posters/jaynes-gallery-usa-california-san-diego-la-jolla-shores-beach-reflects-the-sunset.jpg')
	test_url.append('https://santamonicabeachmom.files.wordpress.com/2011/11/santa-monica-pier-california.jpg?w=600&h=450')
	test_url.append('http://www.inbali.org/wp-content/uploads/2014/07/nusa-dua-bali.jpg')
	test_url.append('http://i1.wp.com/tiomanisland.guide/wp-content/uploads/2015/01/tioman_island_malaysia.jpg')
	test_url.append('http://img1.10bestmedia.com/Images/Photos/96123/captiva-beach-captiva_54_990x660_201404211817.jpg')
	test_url.append('http://langkawibudgetpackages.com/wp-content/uploads/2015/09/beach.jpg')
	test_url.append('http://cdn.pcwallart.com/images/new-york-city-streets-at-night-wallpaper-3.jpg')
	test_url.append('http://www.nationalgeographic.com/new-york-city-skyline-tallest-midtown-manhattan/assets/img/articleImg/01nyskyline1536.jpg')
	test_url.append('http://iliketowastemytime.com/sites/default/files/mumbai-four-seasons-hotel6.jpg')
	test_url.append('http://demo.phpwallpaperscript.com/images/mountain-reflection-in-spitsbergen-norway-wallpaper-for-800x600-39-5.jpg')
	test_url.append('http://www.flarogue7.com/jpgs/jpegs%202/Shadow%20Mountain%20(800%20x%20600).jpg')
	test_url.append('http://static.panoramio.com/photos/large/31242766.jpg')
	test_url.append('http://greenywallpapers.com/wallpapers/10/11870-chile-mountains-torres-del-wallpapers-800x600.jpg')
	test_url.append('http://data.1freewallpapers.com/download/houses-on-the-green-hills-800x600.jpg')
	#random_images
	test_url.append('https://pbs.twimg.com/profile_images/668262727463342080/J2aRvi-0.jpg')
	test_url.append('http://allcinegallery.com/wp-content/gallery/uppi-2-movie-photos-upendra-2-stills/Uppi-2-Movie-Photos-Upendra-2-Stills-02.jpg?3e5e27')
	test_url.append('http://www.worldinternetrankings.com/uploads/bestheavymetalmovies_7110970909.jpg')
	test_url.append('http://cdn.playbuzz.com/cdn/ba85246f-7ab0-4e4d-a32e-96a28a6be47e/1ddd4b3f-23e0-4746-b259-dd5afffd5c8d_560_420.jpg')
	test_url.append('http://static.snopes.com/wordpress/wp-content/uploads/2016/01/friends-reunion-2016.jpg')
	
	
	
	output1 = [];
	for i in range(len(test_url)):
		output1.append(function_visual_rec(test_url[i]))
		print(output1[i])

	count_beach, count_mountain, count_city, count_random = 0, 0, 0, 0
	
	for j in range(len(output1)):
  		if output1[j][0] == 1:
	  		count_beach += 1
	  	elif output1[j][1] == 1:
	  		count_mountain += 1
	  	elif output1[j][2] == 1:
	  		count_city += 1
		elif sum(output1[j]) == 0:
			count_random += 1
			
	total_count = len(output1) - count_random
	print total_count
	print count_beach, count_city, count_mountain
	p_ML_beach = float(count_beach)/total_count
	p_ML_city = float(count_city)/total_count
	p_ML_mountain = float(count_mountain)/total_count
	
	print 'p_ML_beach=',p_ML_beach
	print 'p_ML_city=',p_ML_city
	print 'p_ML_mountain=',p_ML_mountain
	
	
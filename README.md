# videvo_dataset_crawler

Using requests, re, BeautifulSoup to crawl videos from videvo.net  
  
  In this part, you have to run "video_crawler.py" or "video_crawler_by_jupyter.ipynb"  
You'd better use ipynb version by jupyter notebook cuz py file might crash due to requests connection lost.  
  But it could crash as well in a relatively low probability, so when it happens, plz run that program again!  
  This program will automatically create a file called "video", and all the videos would be downloaded there:)
	![effect](https://user-images.githubusercontent.com/60550888/80796735-8f317e80-8bd2-11ea-9184-6b5e317635b0.png)
## Video preprocessing  
In order to do that, plz download the whole project, and rename the file "DataSet" to "video", for this name might be ambiguous when training your dataset.  
Then simply run "video_preprocessing.py" on your pc, then it will automatically create a file named "Frames"  
In this file, you will find 111 subfiles, in which including hell lots of jpg which are the frames of that video.  
I have compressed each frame into 640*360 pixels, and the format is jpg.  
You can customize them in "video_preprocessing.py"  
![effect2](https://user-images.githubusercontent.com/60550888/80834954-5d490800-8c24-11ea-88b3-2a14f19f4c91.png)

Wish you have a nice day:D

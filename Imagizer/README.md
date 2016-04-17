Image Bulk resizer
======================

Introduction
------------

This will resize images in bulk and taking advantage of multi-threading to make it faster

Dependencies
------------

Using Pillow for image manipulation

```
pip install Pillow
```

Usage
-----
the directory and run the program:
```
python imagizer.py
```

To specify input directory:
```
python imagizer.py --input input/
```

To specify output directory:
```
python imagizer.py --destination input/smaller/
```

To specify new image height and width:
```
python imagizer.py --height 900 --width 900
```

To force the new dimentions by using crop functionality
```
python imagizer.py --crop
```

To enable verbose mode for monitoring
```
python imagizer.py --verbose
```

To specify how many threads shal be used at the same time
```
python imagizer.py --threads 4
```

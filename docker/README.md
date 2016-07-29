Generic Classifier Service
---------------------------

To run:
    python generic-app.py -mv /path/to/model/directory

Accepts urls or paths to images in the format
    {
        "url" : "http://somewhere.com/image.jpg"
    }

Returns
    {
        "label" : ... # Whether or not there is a match
        "score" : ... # Whether or not there is a match
        "model" : ... # Model that found the match
    }

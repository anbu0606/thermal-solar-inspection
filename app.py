import os
import os.path
import sys
import signal
import connexion
import darknet
import urllib.request
import urllib.error
import flask
import tempfile
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from flask_httpauth import HTTPBasicAuth
#from OpenSSL import SSL
import ssl
import os

auth=HTTPBasicAuth()
USER_DATA={
    "username" : os.getenv("USERNAME"),
    "password" : os.getenv("PASSWORD")
}

def basic_auth(username, password, required_scopes=None):
    if username == os.getenv("USERNAME") and password == os.getenv("PASSWORD"):
        return {'sub': os.getenv("USERNAME")}
    # Note : Just for validation. 
    # optional: raise exception for custom error response
    return None

@auth.verify_password
def verify(username,password):
    if not(username and password):
        return False
    return ( USER_DATA.get("password") == password and USER_DATA.get("username") == username) 

# Setup handler to catch SIGTERM from Docker
def sigterm_handler(_signo, _stack_frame):
    print('Sigterm caught - closing down')
    sys.exit()

def detect(filename, threshold):
    result = {'classified':[]}
    im = darknet.load_image(bytes(filename, "ascii"), 0, 0)
    r = darknet.detect_image(network, class_names, im, thresh=threshold)
    darknet.free_image(im)
    # Convert confidence from string to float:
    if len(r) > 0:
        for i in range(len(r)):
            xc = r[i][2][0]
            yc = r[i][2][1]
            xmin = int(xc-r[i][2][2]/2)
            xmax = int(xc+r[i][2][2]/2)
            ymin = int(yc-r[i][2][3]/2)
            ymax = int(yc+r[i][2][3]/2)
            result['classified'].append({'label':r[i][0],
                'confidence':float(r[i][1]),'xmin':xmin,'ymin':ymin,
                'xmax':xmax,'ymax':ymax})
            # r[i] = (r[i][0], float(r[i][1]), r[i][2])
    return result

def get_image_type(filename):
    img = Image.open(filename)
    image_type = img.format.lower()
    img.close()
    if not (image_type == 'jpeg' or image_type == 'png'): raise Exception("Image has to be JPEG or PNG")
    return image_type

@auth.login_required
def detect_from_file():
    try:
        file_to_upload = connexion.request.files['image_file']
        threshold = 0.25
        # Use mkstemp to generate unique temporary filename
        fd, filename = tempfile.mkstemp()
        os.close(fd)
        file_to_upload.save(filename)
        image_type = get_image_type(filename)
        os.rename(filename, filename + '.' + image_type)
        filename = filename + '.' + image_type
        res = detect(filename, threshold)
        os.unlink(filename)
        return res
    except urllib.error.HTTPError as err:
        return 'HTTP error', err.code
    except:
        return 'An error occurred', 500


# Load YOLO model:
configPath = "yolov3.cfg"
weightPath = "yolov3_final.weights"
metaPath = "yolov3.data"

network, class_names, class_colors = darknet.load_network(
    configPath,
    metaPath,
    weightPath,
    batch_size=1
)

# Create API:
app = connexion.App(__name__)
# For compatibility we will make the API available both with and without a version basepath
app.add_api('swagger.yaml')
app.add_api('swagger.yaml', base_path='/1.0')

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    context = ssl.SSLContext()
    context.load_cert_chain('/home/app/certs/server_https.crt', '/home/app/certs/server_https.key')
    app.run(port=int(os.environ.get("PORT")), server='gevent',ssl_context=context)

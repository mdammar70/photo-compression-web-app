from flask import Flask, render_template, request
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.pyplot import imread
my_path = os.path.abspath(__file__) # Figures out the absolute path for you in case your working directory moves around.
my_file = 'resnew.png'

app=Flask(__name__)
BASE_PATH=os.getcwd()
UPLOAD_PATH=os.path.join(BASE_PATH,'static/upload')
RESULT_PATH=os.path.join(BASE_PATH,'static/output/result')
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        upload_file=request.files['image_name']
        percentage=int(request.form.get('output'))
        filename=upload_file.filename
        print('The filename that has been Uploaded=',filename)
        ext=filename.split('.')[-1]
        print('Extension of the file is:  ',ext)
        if ext.lower() in ['png','jpg','jpeg']:
            path_save=os.path.join(UPLOAD_PATH,filename)
            upload_file.save(path_save)
            print('File Saved Successfully')
            img = imread(path_save)
            img = img.astype(np.uint8)
            #print(img.shape)
            img = img.mean(axis=2)
            plt.imshow(img, cmap="gray")
            tswizzle_pca = PCA(n_components=percentage).fit(img)
            transformed = tswizzle_pca.transform(img)
            projected = tswizzle_pca.inverse_transform(transformed)
            plt.imshow(projected, cmap="gray")
            plt.axis('off')
            plt.savefig(RESULT_PATH, bbox_inches='tight',pad_inches = 0)  
            return render_template('upload.html',extension=True,fileupload=True)
        else:
            print('Upload Only Images')    
        return render_template('upload.html',extension=True,fileupload=False)
    else:
        return render_template('upload.html',fileupload=False,extension=False)
        

if __name__=="__main__":
    app.run(debug=True)    
    





    
import os
from flask import Flask, render_template, request, redirect, make_response, session,send_from_directory
app = Flask(__name__)

@app.route('/<path:filename>',methods=['GET'])  
def send_file(filename):
    if os.path.isdir(filename):
        remote=request.args.get('remote')
        if not remote:
            remote="false"
        path=filename+"/"
        folders=[i for i in os.listdir(path) if os.path.isdir(path+i)]
        files=[i for i in os.listdir(path) if not os.path.isdir(path+i)]
        units=[' bytes',' KB',' MB',' GB',' TB']
        human_readable= lambda bytes,units:str(bytes) + units[0] if bytes < 1024 else human_readable(bytes>>10, units[1:])
        files_size=[ human_readable(os.stat(path+i).st_size,units) for  i in files ]
        return render_template('localdrive.html',folders=folders,files=files,files_size=files_size,path=path,remote=remote)
    else:
        return send_from_directory("/".join(filename.split("/")[:-1]),filename.split("/")[-1])

if __name__ == '__main__':
    app.run(debug=True)

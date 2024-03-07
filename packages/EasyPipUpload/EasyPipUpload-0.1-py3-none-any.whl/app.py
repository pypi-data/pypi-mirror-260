from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from datetime import datetime
from time import sleep
import subprocess
import shutil
import os

app = Flask(__name__)

Upload_Folder = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = Upload_Folder


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tool = request.form.get('tool').strip()
        tool_name = request.form.get('tool_name').strip()
        ver = request.form.get('ver').strip()
        desc = request.form.get('desc')
        url = request.form.get('url').strip()
        rqrd = request.form.get('rqrd')
        required_files = rqrd.split(",")
        required_files = [x.strip() for x in required_files]
        author = request.form.get('author').strip()

        # Check if any field is empty
        if not tool or not tool_name or not ver or not desc or not url or not rqrd or not author:
            return render_template('index.html', error='Please Fill All Fields')

        if 'file' not in request.files:
            return 'No file part'
        files = request.files.getlist('file')
        for file in files:
            if file and file.filename != '':
                filename = file.filename
                os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], os.path.dirname(filename)), exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        # Check if licence.txt and readme.md exist in any subdirectory
        try :
            subdir = os.listdir(app.config['UPLOAD_FOLDER'])[0]
        except IndexError:
            return render_template('index.html', error='Please Upload Files')
        licence_exists = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], subdir, 'LICENSE.txt'))
        readme_exists = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], subdir, 'readme.md'))

        if not licence_exists:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], subdir, 'LICENSE.txt'), 'w') as f:
                f.write('MIT License\n\n')
                f.write(f'Copyright {datetime.now().year} {author}\n\n')
                f.write(f'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\n')
                f.write(f'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\n')
                f.write(f'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n')


        # if tool not exists then show error
        if tool not in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], subdir)):
            return render_template('index.html', error='IN Folder MAIN FILE Not Found: '+ tool)

        setup_py_loc = os.path.join(app.config['UPLOAD_FOLDER'], subdir, 'setup.py')
        folder = os.path.join(app.config['UPLOAD_FOLDER'], subdir)
        files = [file for file in os.listdir(folder) if file.endswith('.py')]
        files = [file.replace('.py', '') for file in files]
        with open (setup_py_loc,'w') as s_py:
            s_py.write('from setuptools import setup\nimport os\n\n')
            s_py.write('location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))\n')
            s_py.write("readme_loc = os.path.join(location, 'README.md')\n\n")
            s_py.write(f'long_description = open(readme_loc).read()\n')
            s_py.write(f'setup(name="{tool_name}",\n')
            s_py.write(f'version="{ver}",\n')
            s_py.write(f'description="{desc}",\n')
            s_py.write('long_description=long_description,\n')
            s_py.write("long_description_content_type='text/markdown',\n")
            s_py.write(f'author="{author}",\n')
            s_py.write(f'py_modules={files},\n')
            s_py.write(f'url="{url}",\n')
            s_py.write(f'scripts=["{tool}"],\n')
            s_py.write(f'install_requires= {required_files},\n')
            s_py.write("classifiers=[\n    'License :: OSI Approved :: MIT License',\n    'Programming Language :: Python :: 3',\n], )\n")

        if not readme_exists:
            return redirect(url_for('readme'))

        return redirect(url_for('wheel_generator'))
    return render_template('index.html')


@app.route('/readme', methods=['GET', 'POST'])
def readme():
    return render_template('Readme.html')

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    try:
        subdir = os.listdir(app.config['UPLOAD_FOLDER'])[0]
    except Exception:
        return redirect(url_for('index'))
    if 'file' not in request.files:
        return render_template('Readme.html', error='File Not Found')
    file = request.files['file']
    if file.filename == '':
        return render_template('Readme.html', error='Please Upload Files')
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], subdir, filename))
        return redirect(url_for('wheel_generator'))
    return render_template('Readme.html')

@app.route('/download/<filename>')
def download_file(filename):
    src = os.path.join(os.getcwd(),'static', 'wheel', filename)
    return send_file(src, as_attachment=True)

def remove_files():
    try:
        subdir = os.listdir(app.config['UPLOAD_FOLDER'])[0]
        shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], subdir))
        return redirect(url_for('index'))
    except PermissionError:
        sleep(2)
        remove_files()
        return redirect(url_for('upload'))

@app.route('/wheel_generator')
def wheel_generator():
    removal = request.args.get('removal', 'no')
    try:
        subdir = os.listdir(app.config['UPLOAD_FOLDER'])[0]
        if removal == 'yes':
            remove_files()
        setup_py_loc = os.path.join(app.config['UPLOAD_FOLDER'], subdir)
        process = subprocess.Popen(f'cd {setup_py_loc} && python setup.py sdist bdist_wheel',  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            error = f'Error {process.returncode}: {stderr}'
            if "Multiple top-level modules discovered in a flat-layout" in error:
                return f"Error {process.returncode}: {stderr}\n\nPlease Check Your setup.py File\n\n"
        else:
            output = stdout+"\n\nCompleted Successfully\n\nNow You Can Upload Your Package To PyPi\n\n"
            src = os.path.join(setup_py_loc, 'dist')
            # Copy all files from dist to static/uploads/wheel
            dst = os.path.join(os.getcwd(), 'static', 'wheel')
            # Create wheel folder if not exist
            os.makedirs(dst, exist_ok=True)
            for file in os.listdir(src):
                shutil.copy(os.path.join(src, file), dst)
            # list of files
            files =[file for file in os.listdir(src) if os.path.isfile(os.path.join(src, file))]
            # list of urls
            file_urls = [url_for('download_file', filename=file) for file in files]
            return render_template('terminal.html', output=output, file_urls=file_urls)
    except IndexError:
        return redirect(url_for('index'))
    return render_template('terminal.html', file_urls=[])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = "__token__"
        password = request.form.get('password')

        if username and password:
            wheel_files_loc = os.path.join(os.getcwd(), 'static', 'wheel', '*')
            process = subprocess.Popen(f'python -m twine upload --repository pypi --username {username} --password {password} {wheel_files_loc}',  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                error = f'Error {process.returncode}: {stderr}'
                return render_template('upload.html', output=error)
            else:
                return render_template('upload.html', output=stdout)

        else:
            return render_template('upload.html', output='Please Enter Username And Password')
        
    # if os.path.join(os.getcwd(), 'static', 'wheel') is empty then show error
    if not os.listdir(os.path.join(os.getcwd(), 'static', 'wheel')):
        return redirect(url_for('index'))
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')



if __name__ == '__main__':
    app.run(debug=True)
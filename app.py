import os

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# from werkzeug import secure_filename
# from linked_Jobs_US import final_output
# from glob import glob
import jinja2

# import send_mail

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "aress"


# app.jinja_env.filters['zip'] = zip
# # This is the path to the upload directory
# all_folders = ['Final_Output','Output','store_final_data','upload']

# if os.path.exists('Linkedin_data') == False:
#     os.mkdir('Linkedin_data')
# for fldr in all_folders:
#     if os.path.exists(os.getcwd()+"\\Linkedin_data\\"+fldr) == False:
#         os.mkdir(os.getcwd()+"/Linkedin_data/"+fldr)

# upload_path = os.getcwd()+"\\Linkedin_data\\"+"upload\\"

# # store_final_data = r"D:\\Krish\\Krish_Main_Docs\\Projects\\Billable_Projects\\Web_Scraping\\web_service\\store_final_data\\"
# #app.config['UPLOAD_FOLDER'] = upload_path


# @app.route('/')
# def index():
#     location = ["United States","United Kingdom","Australia","New Zealand"]
#     return render_template('linked_index.html',location=location)

# @app.route('/upload', methods=['POST'])
# def upload():
# 	for f in glob(upload_path+"*"):
# 		os.remove(f)
# 	uploaded_files = request.files.getlist("file[]")
# 	filenames = []
# 	for file in uploaded_files:
# 		# if file and allowed_file(file.filename):
# 		filename = secure_filename(file.filename)
# 		file.save(os.path.join(upload_path, filename))
# 		filenames.append(filename)
# 	output_path = os.getcwd()+"\\Linkedin_data\\"+"Output"
# 	for f in glob(output_path+"\*"):
# 		os.remove(f)
# 	if request.method == 'POST':
# 		location = request.form.getlist("loc")
# 	print('Location:#####',location)
# 	domain_file = glob(upload_path+"*.txt")[0]
# 	duration = int(request.form.get("dur"))
# 	dom,locations = final_output(domain_file,location,duration)
# 	final_output_path =os.getcwd()+"\\Linkedin_data\\"+"Final_Output"
# 	filenames = glob(final_output_path+"\*")
# 	names = [i.split('\\')[-1].split('.')[0] for i in filenames]
# 	print("Filenames in upload:####",filenames)
# 	print('Location:#####',location)
# 	print("Names:#####",names)
# 	##send mail
# 	to_mail = request.form.get('mail_id')
# 	send_mail.send(dom,locations,to_address = to_mail)

# 	return render_template('linked_upload.html', filenames=filenames,names=names)

# @app.route('/download/<file_path>', methods=['GET','POST'])
# def download_file(file_path):
#     print("Filename_download:$$$$$$",file_path)
#     name = file_path.split('\\')[-1]
#     path = "\\".join(file_path.split("\\")[:-1])
#     print("Name:$$$$$$",name)
#     print("Path:$$$$$$",path)
#     # files = glob.glob(path+"*")
#     return send_from_directory('Linked_in_Final',file_path)
@app.route('/')
def index():
    # if request.method=='POST' or:
    #     print('Hi')
    return render_template('linked_index - Copy.html')


@app.route('/run_python', methods=['GET', 'POST'])
def run_python():
    if request.method == 'POST' and 'mail_id' in request.form:
        # keywords = document.getElementById('fileinput')
        file = request.files['file']
        if file.filename.endswith('.txt'):        
          content = file.read()
          # return f'The content of the file is: {content}'
          # content=content.split(",")
          content1 = content.decode('UTF-8') 
          content2=content1.split("\r\n")
          print(content2)
        else:
          # return 'Please upload a .txt file'
          print('Please upload a .txt file')
        duration = request.form['dur']
        regions = request.form.getlist('select')
        mail_id = request.form['mail_id']
    
        print("Regions: ", regions)
        
        # print(keywords)
        print("Duration selected: ", duration)
        print("Mail id: ", mail_id)
        print(type(mail_id))
        try:
            
            from Login_Code import Login_linkdin
            driver= Login_linkdin()
            domain_name_list= content2
            locations= regions
            from Extract_data import linkedin_output
            linkedin_output(driver,domain_name_list,locations,mail_id,duration)
           
            print("Inside run_python: ")

            # if (re.findall("Unable", msg) != []):                       
            #     reset_password()
            return render_template('linked_index - Copy.html')
        except Exception as e:
            print("Error: ", e)
            msg = 'Please enter correct password into given area'
            return render_template('linked_index - Copy.html', msg=msg)
        
        


if __name__ == "__main__":
    app.run(debug=True)

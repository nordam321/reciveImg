from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# تحديد المجلد الذي سيتم حفظ الصور فيه
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# تحديد نوع الملف المسموح به
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# دالة للتحقق من امتداد الملف
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# مسار الصفحة الرئيسية
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the image upload API! Use POST on /upload to upload an image."})

# مسار لرفع الصور
@app.route('/upload', methods=['POST'])
def upload_file():
    # تحقق مما إذا كان الطلب يحتوي على ملف
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    # تحقق من أن الملف يحتوي على اسم
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # تحقق من أن الملف له امتداد صحيح
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"message": f"File uploaded successfully: {filename}"}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

# مسار لملف الـ Favicon (اختياري)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)

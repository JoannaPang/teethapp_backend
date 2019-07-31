from flask import render_template, flash, redirect, session, url_for, request, g, Response
from app import app, db, lm, basedir
from .forms import LoginForm, SignupForm, PhotoForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Photo
from .imagetojson import imagetojson, res_json
import logging
from werkzeug.utils import secure_filename
import os, datetime
#from .graphcompute import graph_compute #pang_comment_20190619
from .inference_softmax import batch_inference #pang_add_20190619
from app import model #pang_add_20190619

from flask import send_from_directory
from .token import generate_token, certify_token
import time #pang_add

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template("index.html", 
    title = 'Home', 
    user = user,)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index')) # = redirect(‘/index’)
        
        检查 g.user 是否被设置成一个认证用户，如果是的话将会被重定向到首页。
        这里的想法是如果是一个已经登录的用户的话，就不需要二次登录了
        Flask 中的 g 全局变量是一个在请求生命周期中用来存储和共享数据
        
    '''    
    form = LoginForm()
    app.logger.debug(form.name.data)
    app.logger.debug(form.psw.data)
    app.logger.debug(form.submit.data)
#    if form.validate_on_submit():
    user = User.query.filter_by(name = form.name.data).first()
    if user is not  None and user.psw == form.psw.data:
        login_user(user)
        app.logger.debug('login')
        token = generate_token(form.name.data)
        return res_json(token)
    else:
        app.logger.debug('cannot login')
        return 'wrong password'
        '''
        oid.try_login 被调用是为了触发用户使用 Flask-OpenID 认证。
        该函数有两个参数，用户在 web 表单提供的 openid 以及我们从 OpenID 提供商得到的数据项列表
        '''
    app.logger.debug('unsafe data')
#    return 'data unsafe'
    """
    validate_on_submit 方法做了所有表单处理工作。当表单正在展示给用户的时候调用它，它会返回 False.
    如果 validate_on_submit 在表单提交请求中被调用，它将会收集所有的数据，对字段进行验证，如果所有的事情都通过的话，它将会返回 True，
    表示数据都是合法的。这就是说明数据是安全的，并且被应用程序给接受了。
    如果至少一个字段验证失败的话，它将会返回 False，接着表单会重新呈现给用户，这也将给用户一次机会去修改错误。
    我们将会看到当验证失败后如何显示错误信息。
    当 validate_on_submit 返回 True，我们的登录视图函数调用了两个新的函数，
    导入自 Flask。flash 函数是一种快速的方式下呈现给用户的页面上显示一个消息。
    在我们的例子中，我将会使用它来调试，因为我们目前还不具备用户登录的必备的基础设施，
    相反我们将会用它来显示提交的数据。flash 函数在生产服务器上也是十分有作用的，用来提供反馈给用户有关的行动。
    """
@lm.user_loader
def load_user(id):
    return User.query.get(int(id)) #在 Flask-Login 中的用户 ids 永远是 unicode 字符串

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    app.logger.debug(form.name.data)
    app.logger.debug(form.psw.data)
    app.logger.debug(form.email.data)
    app.logger.debug(form.submit.data)
    #resp 参数传入给 after_login 函数，它包含了从 OpenID 提供商返回来的信息。
#    if form.name.data is None or form.name.data == "":
#        form.name.data = form.email.data.split('@')[0]
    useremail = User.query.filter_by(email = form.email.data).first()
    usernickname = User.query.filter_by(name = form.name.data).first()
    if useremail is not  None:
        return 'this email cannot use'
    if usernickname is not  None:
        return 'this nickname cannot use'
    user = User(name = form.name.data, email = form.email.data, psw = form.psw.data)
#   , email = form.email.data)
    db.session.add(user)
    db.session.commit()
    return 'signup successfully' 
'''
@app.before_request
def before_request():
    g.user = current_user
'''    
@app.route('/logout')
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('index'))

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        starttime = time.time() #pang_add
        f = request.files['file']
        username = request.form['Username']
        day = request.form['Date']
        app.logger.debug(username)
        app.logger.debug(day)
        app.logger.debug(f)
        app.logger.debug(f.content_length)
        filename = secure_filename(f.filename)
        filetype = filename.split('.')[1]
        date1 = str(datetime.datetime.now()).split('.')[0].replace('-','')
        date2 = date1.split(' ')[0] + 'd' + date1.split(' ')[1]
        date3 = date2.split(':')[0] + 'h' + date2.split(':')[1] + 'm' + date2.split(':')[2] + 's'
        filename = date3 + '.' + filetype
        app.logger.debug(filename)
#        types = ['jpg', 'png', 'gif']
#        app.logger.debug(filename.split('.')[-1])
#        if filename.split('.')[-1] in types:
        #dir_name = os.path.join(basedir, 'static\\uploads', username, day) #pang_comment
        dir_name = os.path.join(basedir, 'static/uploads', username, day) #pang_fix
        upload_path = os.path.join(dir_name, filename)
        app.logger.debug(upload_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            '''
        else:
            for filename in os.listdir(dir_name):
                if os.path.isfile(os.path.join(dir_name, filename)):
                     os.remove(os.path.join(dir_name, filename))
                     '''
        f.save(upload_path)
        app.logger.debug('tensorflow start run')

        #resultpath, ratio = graph_compute(upload_path) #pang_comment_20190619
        resultpath, ratio = batch_inference(model, upload_path) #pang_add_20190619

        app.logger.debug(ratio)
        app.logger.debug(resultpath)
        user = User.query.filter_by(name = username).first()
        #photo = Photo(update_time = datetime.datetime.now(), photo_path = upload_path, #pang_comment_20190703
        #            result_path = resultpath, user_id = user.id) #pang_comment_20190703
        photo = Photo(update_time = datetime.datetime.now(), photo_path = upload_path, #pang_fix_20190703
                    result_path = resultpath, ratio = ratio, user_id = user.id) #pang_fix_20190703


        db.session.add(photo)
        db.session.commit()
#          return redirect(url_for('upload'))
        app.logger.debug('saved')
        #result_path = resultpath.split('\\')[len(resultpath.split('\\'))-1] #pang_comment
        result_path = resultpath.split('/')[len(resultpath.split('/'))-1] #pang_fix
        app.logger.debug(result_path)
        jsonpath = imagetojson(resultpath, ratio)
        #result_path = jsonpath.split('\\')[len(jsonpath.split('\\'))-1] #pang_comment
        result_path = jsonpath.split('/')[len(jsonpath.split('/'))-1] #pang_fix
        '''
        m = MultipartEncoder(
            fields = {'ratio' : ratio,
            'field2' : ('dir_name', open(resultpath, 'rb'), 'image/jpeg')}
            )
        '''
        app.logger.debug('ok')
        endtime = time.time() #pang_add
        usingtime = endtime - starttime #pang_add
        app.logger.debug('using time(s):') #pang_add
        app.logger.debug(usingtime) #pang_add
        return send_from_directory(dir_name, result_path, as_attachment=True)
#        return Response(m.to_string(), mimetype = m.content_type)
#        else:
#            return 'error file type'
    else:
#        return render_template('upload.html')
         return 'not post'

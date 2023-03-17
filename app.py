from flask import Flask, request, jsonify
import jwt
from functools import wraps
import datetime
import psycopg2


def db_connect():
    conn = psycopg2.connect(database="Reunion_DB", user="postgres", password="rootroot", host="database-1.c068glaizvq1.us-east-1.rds.amazonaws.com", port="5432")
    # cur = conn.cursor()
    return conn
    # cur.execute("select * from Users")
    # data = cur.fetchall()
    # print(len(data[0][1]))


def db_close(conn):
    conn.commit()
    conn.close()


def current_user():
    token = request.form['token']

    # print(token, type(token))
    data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
    # print(data)
    return data['id'], data['user'], data['password']


app = Flask(__name__)


app.config['SECRET_KEY'] = "Reunion_is_best"


def token_req(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        token = request.form['token']
        if not token:
            return jsonify({'Status': 'No Token available'})

        try:
            # print(token, type(token))
            data = jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
            print('token-data', data)
        except :
            return jsonify({'Status': 'Token is wrong'})
        return fun(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    return "This is Home"


@app.route('/api/authenticate')
def login():
    email = request.args.get('email')
    password = request.args.get('pass')
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(f"select * from Users where email='{email}' and password='{password}';")
        data = cur.fetchone()

        id = data[0]
        # print(data,id)
        # print(email, password)
        if data:
            token = jwt.encode({'id': id, 'user': email, 'password': password}, key=app.config['SECRET_KEY'])
            # print(type(token))
            db_close(conn)
            return jsonify({'Email': email,
                'Password': password,
                'token': token})
    except:
        db_close(conn)
        return jsonify({
            'status': 'Decline',
            'Reason': 'Credential Invalid'
    })


@app.route('/api/follow/<id>', methods=["POST"])
@token_req
def follow_action(id):
    if request.method == 'POST':
        # print(id)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(f'select * from Users where id={id};')
        data = cur.fetchone()
        if data:
            current_id, current_email, current_pass = current_user()

            # print('current user id=',current_id[0])
            cur.execute(f"Select * from Follow where user_id='{current_id}' and follow_id={id};")
            follows_count = cur.fetchone()
            if follows_count:
                db_close(conn)
                return jsonify({
                    'message': 'You already follow this User'
                })
            else:
                cur.execute(f"Insert into follow values({current_id}, {id});")
                db_close(conn)
                return jsonify({
                    'message': 'Successfully follow this User'
                })

        else:
            db_close(conn)
            return jsonify({'Message': 'No such user exist'})


@app.route('/api/unfollow/<id>', methods=['POST'])
@token_req
def unfollow_action(id):
    if request.method == "POST":
        conn = db_connect()
        cur = conn.cursor()
        cur.execute(f'select * from Users where id={id};')
        data = cur.fetchone()
        if data:
            current_id, current_email, current_pass = current_user()
            cur.execute(f"delete from Follow where user_id={current_id} and follow_id={id};")
            db_close(conn)
            return jsonify({
                'message': 'Successfully unfollow the user'
            })
        else:
            db_close(conn)
            return jsonify({'Message': 'No such user exist'})


@app.route('/api/user')
@token_req
def user():
    conn = db_connect()
    cur = conn.cursor()
    current_id, current_email, current_pass = current_user()
    cur.execute(f"Select * from Users where email='{current_email}' and password='{current_pass}';")
    data = cur.fetchone()
    user_name = data[1]
    cur.execute(f"select count(*) from Follow where user_id={current_id};")
    following = cur.fetchone()[0]
    cur.execute(f"select count(*) from Follow where follow_id={current_id};")
    followers = cur.fetchone()[0]

    # print(current_id, user_name)
    # print(following, followers)
    db_close(conn)
    return jsonify({'Name': user_name,
                    'Followers': followers,
                    'Following': following
                    })


@app.route('/api/posts', methods=["POST"])
@token_req
def create_post():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        conn = db_connect()
        cur = conn.cursor()
        current_id, current_email, current_pass = current_user()

        cur.execute(f"Insert into Posts(title,description,user_id) values('{title}','{description}','{current_id}');")
        db_close(conn)
        return jsonify({"message": 'Successfully upload a post'})


@app.route('/api/posts/<id>', methods=["DELETE"])
@token_req
def delete_post(id):
    if request.method == "DELETE":
        conn = db_connect()
        cur = conn.cursor()
        current_id, current_email, current_pass = current_user()

        cur.execute(f"Select * from Posts where post_id='{id}' and user_id='{current_id}';")
        data = cur.fetchone()
        if data:
            cur.execute(f"delete from Posts where post_id='{id}'")
            db_close(conn)
            return jsonify({'message': 'Post delete Successfully'})
        else:
            db_close(conn)
            return jsonify({"message":"This Post is not posted by you. So, you dont have permission to delete it."})


@app.route('/api/like/<id>', methods=["POST"])
@token_req
def like_post(id):
    if request.method == 'POST':
        conn = db_connect()
        cur = conn.cursor()
        current_id, current_email, current_pass = current_user()
        cur.execute(f"select * from Posts where post_id={id}")
        data = cur.fetchone()
        if data:
            cur.execute(f"select * from userlikes where user_id={current_id} and post_id={id};")
            already_liked = cur.fetchall()
            if not already_liked:
                cur.execute(f"insert into userlikes values({current_id},{id})")
                db_close(conn)
                return jsonify({'message': 'Liked post successfully'})
            else:
                db_close(conn)
                return jsonify({'message': 'Post is already liked'})
        else:
            return jsonify({'message': 'Post does not exist'})


@app.route('/api/unlike/<id>', methods=["POST"])
@token_req
def unlike_post(id):
    if request.method == 'POST':
        conn = db_connect()
        cur = conn.cursor()
        current_id, current_email, current_pass = current_user()
        cur.execute(f"select * from Posts where post_id={id}")
        data = cur.fetchone()
        if data:
            cur.execute(f"select * from userlikes where user_id={current_id} and post_id={id};")
            liked_post = cur.fetchone()
            if liked_post:
                cur.execute(f"delete from userlikes where user_id={current_id} and post_id={id};")
                db_close(conn)
                return jsonify({
                    'message': 'Unlike Successfully'
                })
            else:
                db_close(conn)
                return jsonify({
                    'message': 'Post already unlike'
                })
        else:
            db_close(conn)
            return jsonify({
                'message': 'Post does not exist'
            })


@app.route('/api/comment/<post_id>', methods=["POST"])
@token_req
def add_comment(post_id):
    if request.method == 'POST':
        comment = request.form['comment']
        conn = db_connect()
        cur = conn.cursor()
        current_id, current_email, current_pass = current_user()
        cur.execute(f"select * from Posts where post_id={post_id}")
        data = cur.fetchone()
        if data:
            cur.execute(f"insert into comments values({post_id}, '{comment}', {current_id});")
            db_close(conn)
            return jsonify({
                'message': 'Comment added successfully'
            })
        else:
            db_close(conn)
            return jsonify({'message': 'Post id does not exist'})


@app.route('/api/post/<post_id>')
def post_details(post_id):
    conn = db_connect()
    cur = conn.cursor()
    # current_id, current_email, current_pass = current_user()

    cur.execute(f"select * from Posts where post_id={post_id}")
    data = cur.fetchone()
    if data:
        cur.execute(f"select count(*) from userlikes where post_id={post_id};")
        no_of_likes = cur.fetchone()[0]
        cur.execute(f"select comment from comments where post_id={post_id};")
        all_comments = cur.fetchall()

        db_close(conn)
        return jsonify({
            'Post id': post_id,
            'Number of likes': no_of_likes,
            'Comments': all_comments
        })
    else:
        db_close(conn)
        return jsonify({'message': 'Post id does not exist'})


@app.route('/api/all_post')
@token_req
def all_post():
    conn = db_connect()
    cur = conn.cursor()
    current_id, current_email, current_pass = current_user()
    cur.execute(f"select * from Posts where user_id={current_id} order by create_time")
    all_post = cur.fetchall()
    # print(all_post)
    post_id = []
    post_title = []
    post_desc = []
    post_date = []
    post_likes = []
    comments = []
    print("fetching all Post data--")
    for post in all_post:
        # print(post[0])
        post_id.append(post[0])
        cur.execute(f"select comment from comments where post_id={post[0]};")
        comment = [x[0] for x in cur.fetchall()]
        # print(comment)
        comments.append(comment)
        post_title.append(post[1])
        post_desc.append(post[2])
        post_date.append(post[3])
        cur.execute(f"select count(*) from userlikes where post_id={post[0]};")
        total_likes = cur.fetchone()[0]
        post_likes.append(total_likes)

    return jsonify({
        'id': post_id,
        'Title': post_title,
        'Description': post_desc,
        'Created time': post_date,
        'Likes': post_likes,
        'Comments': comments
    })


@app.route('/vaah')
def vaah():
    return jsonify({'status': 'inside vaah'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

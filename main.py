import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Временная "база данных" в памяти
forum_data = {
    1: {
        "title": "Первая тема на форуме!",
        "content": "Привет всем! Это наше новое приложение.",
        "comments": ["Круто!", "Отличный старт!"]
    }
}
next_id = 2


@app.route('/')
def index():
    return render_template('index.html', topics=forum_data)


@app.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    if topic_id not in forum_data:
        return "Тема не найдена", 404

    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            forum_data[topic_id]['comments'].append(comment)
        return redirect(url_for('topic', topic_id=topic_id))

    return render_template('topic.html', topic=forum_data[topic_id], topic_id=topic_id)


@app.route('/create', methods=['POST'])
def create_topic():
    global next_id
    title = request.form.get('title')
    content = request.form.get('content')

    if title and content:
        forum_data[next_id] = {
            "title": title,
            "content": content,
            "comments": []
        }
        next_id += 1
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Настройки для запуска на Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
from web import app
from flask import render_template, session, redirect, url_for
from web.forms import LoginForm, Level1Form, Level2Form, Level3Form, Level4Form
from web.service import read_auth_data
from web.helper import cur_user, update_user_level


@app.route('/')
def main():
    return redirect(url_for('auth'))


@app.route('/game')
def game():
    user = cur_user()
    if user is None:
        return redirect(url_for('auth'))
    if user.level != -1:
        return redirect(url_for('game_level', level=user.level))
    return render_template('game.html', user=user, title='Игра')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    auth_form = LoginForm()

    if auth_form.validate_on_submit():
        users_holder = read_auth_data()
        check = users_holder.check_logpas(auth_form.login.data, auth_form.password.data)
        if check == 1:
            auth_form.login.errors.append('Неизвестный логин')
        if check == 2:
            auth_form.password.errors.append('Неправильный пароль')
        if check == 0:
            session['login'] = auth_form.login.data
            return redirect(url_for('game'))
    return render_template('auth_page.html', form=auth_form, title="Вход", user=cur_user())


@app.route('/game/<int:level>', methods=['GET', 'POST'])
def game_level(level):
    max_level = 5
    user = cur_user()
    if user is None:
        return redirect(url_for('auth'))
    if user.level < level and user.level != -1:
        return redirect(url_for('game_level', level=user.level))
    if level > max_level or level < 1:
        return redirect(url_for('game_level', level=user.level))

    if level == max_level:
        return render_template('the_end.html', title='Конец', user=user)
    if level == 1:
        return level_1(user)
    if level == 2:
        return level_2(user)
    if level == 3:
        return level_3(user)
    if level == 4:
        return level_4(user)

    return render_template('game_'+str(level)+'.html', title='Уровень '+str(level), user=user)


def level_1(user):
    form = Level1Form()
    if form.validate_on_submit():
        if user.level == 1:
            update_user_level(user.login, 2)
        return redirect(url_for('game_level', level=2))
    return render_template('game_1.html', title='Уровень 1', user=user, form=form)


def level_2(user):
    form = Level2Form()
    error = None
    if form.is_submitted():
        string = form.let1.data + form.let2.data + form.let3.data \
                 + form.let4.data + form.let5.data + form.let6.data + form.let7.data
        if string.lower() == 'счастье':
            if user.level == 2:
                update_user_level(user.login, 3)
            return redirect(url_for('game_level', level=3))
        error = '"{}" — не "счастье"'.format(string)
    return render_template('game_2.html', title='Уровень 2', user=user, form=form, error=error)


def level_3(user):
    form = Level3Form()
    error = None
    if form.validate_on_submit():
        if form.pic1.data == '2' and form.pic2.data == '3' and form.pic3.data == '5' and \
                form.pic4.data == '6' and form.pic5.data == '4' and form.pic6.data == '1':
            if user.level == 3:
                update_user_level(user.login, 4)
            return redirect(url_for('game_level', level=4))
        error = 'Неправильный порядок'

    return render_template('game_3.html', title='Уровень 3', user=user, form=form, error=error)


def level_4(user):
    form = Level4Form()
    stage = session.get('lvl4')
    error = None

    if stage is None:
        session['lvl4'] = 'val'
        stage = 'val'

    if not form.validate_on_submit():
        return render_template('game_4.html', title='Уровень 4', user=user, form=form, stage=stage, error=error)

    user_ans = form.answer.data.lower()
    if stage == 'val' and 'fissman' in user_ans:
        stage = 'biz'
        session['lvl4'] = 'biz'
        return redirect(url_for('game_level', level=4))
    elif stage == 'biz' and 'изюбрь' in user_ans:
        stage = 'int'
        session['lvl4'] = 'int'
        return redirect(url_for('game_level', level=4))
    elif stage == 'int' and ('1/4 тона' in user_ans or 'четверть тона' in user_ans):
        stage = 'prk'
        session['lvl4'] = 'prk'
        return redirect(url_for('game_level', level=4))
    elif stage == 'prk' and 'шредер' in user_ans:
        if user.level == 4:
            update_user_level(user.login, 5)
        return redirect(url_for('game_level', level=5))
    else:
        error = 'Неверный ответ'
    return render_template('game_4.html', title='Уровень 4', user=user, form=Level4Form(), stage=stage, error=error)


@app.route('/logout')
def logout():
    if 'login' in session:
        session.clear()
    return redirect(url_for('auth'))


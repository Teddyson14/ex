from flask import Flask, render_template, request, redirect, url_for, flash, session

from database import db

from model import Users, Products



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ex.db'

app.secret_key = 'your-secret-key'

db.init_app(app)





@app.route('/')

def login():

    return render_template('login.html')





@app.route('/auth', methods=['POST'])

def auth():

    login_input = request.form.get('login')

    password = request.form.get('password')

    guest_mode = request.form.get('guest_mode')



    # Если нажали "Войти как гость"

    if guest_mode:

        session['user_id'] = None

        session['user_login'] = 'гость'

        session['user_fio'] = 'Гостевой пользователь'

        session['user_role'] = 'гость'

        flash('Вы вошли как гость', 'info')

        return redirect(url_for('products'))



    # Обычный вход с логином и паролем

    if not login_input or not password:

        flash('Заполните все поля', 'danger')

        return redirect(url_for('login'))



    user = Users.query.filter_by(login=login_input, password=password).first()



    if user:

        session['user_id'] = user.id

        session['user_login'] = user.login

        session['user_fio'] = user.fio

        session['user_role'] = user.role

        flash(f'Добро пожаловать, {user.fio}!', 'success')

        return redirect(url_for('products'))

    else:

        flash('Неверный логин или пароль', 'danger')

        return redirect(url_for('login'))





@app.route('/main')

def main():

    if 'user_role' not in session:

        return redirect(url_for('login'))

    all_products = Products.query.all()

    return render_template('main.html', products=all_products)





@app.route('/products')

def products():

    if 'user_role' not in session:

        return redirect(url_for('login'))



    all_products = Products.query.all()

    return render_template('products.html', products=all_products)

# Универсальный роут: если article передан — редактируем, если нет — создаем новый
@app.route('/products/edit/', defaults={'product_article': None}, methods=['GET', 'POST'])
@app.route('/products/edit/<path:product_article>', methods=['GET', 'POST'])
def edit_product(product_article):
    # Ищем товар по его первичному ключу article
    product = Products.query.get(product_article) if product_article else None

    if request.method == 'POST':
        # Собираем данные из полей HTML-формы
        data = {
            'name': request.form.get('name'),
            'unit': request.form.get('unit', 'шт.'),
            'price': float(request.form.get('price', 0)),
            'discount': float(request.form.get('discount', 0)),
            'category': request.form.get('category'),
            'manufacturer': request.form.get('manufacturer'),
            'supplier': request.form.get('supplier'),
            'description': request.form.get('description'),
            'amount': int(request.form.get('amount', 0)),
            'src_img': request.form.get('src_img') or 'default.jpg'
        }

        if product:
            # РЕДАКТИРОВАНИЕ: обновляем существующий товар (артикул менять нельзя, он PK)
            for key, value in data.items():
                setattr(product, key, value)
        else:
            # СОЗДАНИЕ: при создании нового товара записываем и сам артикул из формы
            data['article'] = request.form.get('article')
            product = Products(**data)
            db.session.add(product)

        db.session.commit()
        return redirect(url_for('products'))

    return render_template('redact.html', product=product)

@app.route('/product/delete/<path:product_article>', methods=['GET'])
def delete_product(product_article):
    # Ищем товар по артикулу
    product = Products.query.get_or_404(product_article)
    
    # Удаляем из сессии и сохраняем изменения
    db.session.delete(product)
    db.session.commit()
    
    # Возвращаемся на главную страницу
    return redirect(url_for('products'))

@app.route('/logout')

def logout():

    session.clear()

    flash('Вы вышли из системы', 'info')

    return redirect(url_for('login'))





if __name__ == '__main__':

    app.run(debug=True)
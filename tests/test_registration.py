import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
def test_add_existing_user(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    add_user('ttt', 'yyy', 'zzz')
    assert add_user('ttt', 'yyy2', 'zzz2') == False, "Добавление пользователя с существующим логином должно вернуть False."

def test_authenticate_user(setup_database, connection):
    add_user('rrr', 'ccc', 'ddd')
    assert authenticate_user('rrr', 'ddd') == True

def test_authenticate_nonexistent_user(setup_database, connection):
    assert authenticate_user('nonexistent', 'password') == False

def test_authenticate_user_with_wrong_password(setup_database, connection):
    add_user('aaa', 'bbb', 'ccc')
    assert authenticate_user('aaa', 'wrongpassword') == False

def test_display_users(setup_database, connection):
    add_user('user1', 'user2', 'user3')
    users = display_users()
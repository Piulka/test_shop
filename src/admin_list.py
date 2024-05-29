def read_admin_list():
    try:
        with open('../admins.txt', 'r') as file:
            admin_list = [line.strip() for line in file]
    except FileNotFoundError:
        admin_list = []
    return admin_list


def add_admin(user_id):
    admin_list = read_admin_list()
    if user_id not in admin_list:
        print(user_id)
        with open('../admins.txt', 'w') as file:
            for admin_id in admin_list:
                file.write(f'{admin_id}\n')


def is_admin(user_id):
    admin_list = read_admin_list()
    return str(user_id) in admin_list  # Преобразуем user_id в строку перед проверкой

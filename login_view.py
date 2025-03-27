import flet as ft
from database import Database

db = Database()

def login_view(page: ft.Page):
    def login(e):
        if db.validate_user(username.value, password.value):
            page.session.set("user", username.value)
            page.go("/main")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Credenciais inválidas!"))
            page.snack_bar.open = True
        page.update()

    def signup(e):
        if db.create_user(username.value, password.value):
            page.snack_bar = ft.SnackBar(ft.Text("Usuário criado com sucesso!"))
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuário já existe!"))
            page.snack_bar.open = True
        page.update()

    username = ft.TextField(label="Usuário", autofocus=True)
    password = ft.TextField(label="Senha", password=True)
    
    return ft.View(
        "/",
        controls=[
            ft.AppBar(title=ft.Text("Login")),
            ft.Text("Gestão de Humor", size=30),
            username,
            password,
            ft.Row([
                ft.ElevatedButton("Entrar", on_click=login),
                ft.ElevatedButton("Cadastrar", on_click=signup)
            ])
        ]
    )
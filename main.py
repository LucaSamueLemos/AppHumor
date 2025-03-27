import flet as ft
from login_view import login_view
from main_view import main_view
from calendar_view import calendar_view
from database import Database

def main(page: ft.Page):
    # Configuração inicial do app
    page.title = "Gestão de Humor 2.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Inicializa o banco de dados
    db = Database()

    # Configura o sistema de rotas
    def route_change(route):
        page.views.clear()
        
        # Tela de Login
        if page.route == "/":
            page.views.append(login_view(page))
            
        # Tela Principal
        elif page.route == "/main":
            page.views.append(main_view(page))
            
        # Tela do Calendário
        elif page.route == "/calendar":
            page.views.append(calendar_view(page))
        
        page.update()

    # Configuração dos eventos de navegação
    page.on_route_change = route_change
    page.go(page.route)

# Executa o aplicativo
if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8000
    )
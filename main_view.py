import flet as ft
from datetime import datetime
from database import Database

db = Database()

def main_view(page: ft.Page):
    emotions = ['😊 Feliz', '😢 Triste', '😡 Raiva', '😲 Surpreso', '😰 Ansioso', '😌 Calmo']
    selected_emotion = ft.Dropdown(options=[ft.dropdown.Option(e) for e in emotions])
    chat_history = ft.ListView(expand=True)
    notes_field = ft.TextField(label="Notas adicionais", multiline=True, expand=True)
    user_message = ft.TextField(label="Digite sua mensagem", expand=True)

    def send_message(e):
        if user_message.value:
            chat_history.controls.append(ft.Text(f"Você: {user_message.value}"))
            chat_history.controls.append(ft.Text("IA: Como posso ajudá-lo com isso?"))
            user_message.value = ""
            page.update()

    def save_entry(e):
        user_id = page.session.get("user_id")
        if user_id and selected_emotion.value:
            chat_text = "\n".join([c.value for c in chat_history.controls])
            db.save_mood_entry(
                user_id=user_id,
                emotion=selected_emotion.value,
                notes=notes_field.value,
                chat_history=chat_text
            )
            page.snack_bar = ft.SnackBar(ft.Text("Registro salvo com sucesso!"))
            page.snack_bar.open = True
            page.update()

    return ft.View(
        "/main",
        controls=[
            ft.AppBar(title=ft.Text("Registro Diário"), actions=[
                ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=lambda _: page.go("/calendar")),
                ft.IconButton(ft.Icons.LOGOUT, on_click=lambda _: page.go("/"))
            ]),
            ft.Text("Selecione seu humor:", size=20),
            selected_emotion,
            ft.Divider(),
            ft.Text("Chat com IA:", size=16),
            chat_history,
            ft.Row([user_message, ft.IconButton(ft.Icons.SEND, on_click=send_message)]),
            ft.Text("Notas:", size=16),
            notes_field,
            ft.ElevatedButton("Salvar Registro", on_click=save_entry)
        ]
    )
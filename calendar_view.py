import flet as ft
import calendar
from datetime import datetime
from database import Database

db = Database()

class Calendar:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_date = datetime.now()
        self.grid = ft.GridView(
            expand=True,
            runs_count=7,
            max_extent=100,
            spacing=5,
            run_spacing=5
        )
        self.entries = []
        self.load_entries()

    def load_entries(self):
        user_id = self.page.session.get("user_id")
        self.entries = db.get_month_entries(
            user_id=user_id,
            year=self.current_date.year,
            month=self.current_date.month
        )

    def create_header(self):
        return ft.Row([
            ft.IconButton(
                ft.icons.CHEVRON_LEFT,
                on_click=lambda _: self.change_month(-1)
            ),
            ft.Text(
                f"{self.current_date.strftime('%B %Y').upper()}",
                size=20,
                weight=ft.FontWeight.BOLD
            ),
            ft.IconButton(
                ft.icons.CHEVRON_RIGHT,
                on_click=lambda _: self.change_month(1)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def change_month(self, delta):
        month = self.current_date.month + delta
        year = self.current_date.year
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
            
        self.current_date = datetime(year, month, 1)
        self.load_entries()
        self.update_calendar()

    def get_day_entries(self, day):
        target_date = f"{self.current_date.year}-" \
                     f"{self.current_date.month:02}-" \
                     f"{day:02}"
        return [entry for entry in self.entries 
                if entry[0].startswith(target_date)]

    def create_day_content(self, day, is_current_month):
        entries = self.get_day_entries(day)
        content = []
        
        if is_current_month:
            content.append(ft.Text(str(day), size=12))
            if entries:
                emotion = entries[0][1].split()[0]  # Pega o emoji
                content.append(ft.Text(emotion, size=20))
                
        return ft.Column(
            content,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def create_day(self, day, is_current_month):
        entries = self.get_day_entries(day)
        return ft.Container(
            content=self.create_day_content(day, is_current_month),
            width=100,
            height=100,
            border=ft.border.all(0.5, ft.colors.OUTLINE),
            bgcolor=ft.colors.SURFACE_VARIANT if entries else None,
            on_click=lambda e, d=day: self.show_day_details(d) if is_current_month else None,
            tooltip=f"Clique para detalhes" if is_current_month else None
        )

    def update_calendar(self):
        self.grid.controls.clear()
        
        cal = calendar.Calendar()
        month_days = cal.monthdays2calendar(
            self.current_date.year, 
            self.current_date.month
        )

        # Cabeçalho com dias da semana
        week_days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for day in week_days:
            self.grid.controls.append(
                ft.Container(
                    content=ft.Text(day, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    width=100,
                    height=30
                )
            )

        # Dias do calendário
        for week in month_days:
            for day, weekday in week:
                if day == 0:
                    # Dia do mês anterior/próximo
                    self.grid.controls.append(
                        ft.Container(
                            content=ft.Text(""),
                            border=ft.border.all(0.5, ft.colors.OUTLINE),
                            bgcolor=ft.colors.BACKGROUND
                        )
                    )
                else:
                    self.grid.controls.append(
                        self.create_day(day, True)
                    )

        self.page.update()

    def show_day_details(self, day):
        entries = self.get_day_entries(day)
        if not entries:
            return
        
        content = []
        for entry in entries:
            date = datetime.strptime(entry[0], "%Y-%m-%d %H:%M:%S")
            content.extend([
                ft.Text(f"Data: {date.strftime('%d/%m/%Y %H:%M')}"),
                ft.Text(f"Emoção: {entry[1]}"),
                ft.Text(f"Notas: {entry[2] or 'Sem notas'}"),
                ft.Divider()
            ])
        
        dialog = ft.AlertDialog(
            title=ft.Text(f"Detalhes do dia {day}"),
            content=ft.Column(content, scroll=ft.ScrollMode.ALWAYS),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: self.close_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()

def calendar_view(page: ft.Page):
    calendar = Calendar(page)
    calendar.update_calendar()
    
    return ft.View(
        "/calendar",
        controls=[
            ft.AppBar(
                title=ft.Text("Calendário"),
                actions=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: page.go("/main")
                    )
                ]
            ),
            calendar.create_header(),
            ft.Container(
                content=calendar.grid,
                margin=ft.margin.all(20),
            ),
            ft.FloatingActionButton(
                icon=ft.icons.ARROW_BACK,
                text="Voltar",
                on_click=lambda _: page.go("/main")
            )
        ]
    )
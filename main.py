import flet as ft
import datetime


def login_page(page: ft.Page):
    email = ft.TextField(label="Email", width=260)
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=260,
    )
    remember = ft.Checkbox(label="Remember me")
    error = ft.Text(color="red", size=12)

    def login(e):
        error.value = ""
        if email.value == "" or password.value == "":
            error.value = "Please fill all fields"
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Login successful"), open=True)
        page.update()

    login_btn = ft.ElevatedButton(
        text="Login",
        width=260,
        on_click=login,
    )

    create_btn = ft.TextButton(
        text="Create account",
        on_click=lambda e: page.go("/register"),
    )

    card = ft.Card(
        content=ft.Container(
            padding=20,
            width=320,
            content=ft.Column(
                [
                    ft.Text("Sign in", size=20, weight=ft.FontWeight.BOLD),
                    email,
                    password,
                    remember,
                    error,
                    login_btn,
                    create_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                tight=True,
            ),
        )
    )

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.GREY_100,
        content=card,
    )


def register_page(page: ft.Page):
    name = ft.TextField(label="Name", width=260)
    email_r = ft.TextField(label="Email", width=260)
    password_r = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=260,
    )
    confirm_r = ft.TextField(
        label="Confirm password",
        password=True,
        can_reveal_password=True,
        width=260,
    )
    gender = ft.Dropdown(
        label="Gender",
        width=260,
        options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")],
    )
    dob = ft.TextField(label="Date of birth (dd.mm.yyyy)", width=260)
    error_r = ft.Text(color="red", size=12)

    def register(e):
        error_r.value = ""

        if (
            name.value == ""
            or email_r.value == ""
            or password_r.value == ""
            or confirm_r.value == ""
        ):
            error_r.value = "Fill all fields"
        elif any(ch.isdigit() for ch in name.value):
            error_r.value = "Name cannot contain numbers"
        elif email_r.value.isdigit():
            error_r.value = "Email cannot be a number"
        elif "@" not in email_r.value:
            error_r.value = "Invalid email format"
        elif len(password_r.value) < 6:
            error_r.value = "Password must be at least 6 characters"
        elif not any(ch.isdigit() for ch in password_r.value):
            error_r.value = "Password must contain a number"
        elif password_r.value != confirm_r.value:
            error_r.value = "Passwords do not match"
        elif gender.value is None:
            error_r.value = "Select gender"
        elif dob.value == "":
            error_r.value = "Enter date of birth"
        else:
            try:
                birth = datetime.datetime.strptime(dob.value, "%d.%m.%Y")
                today = datetime.datetime.today()
                age = (today - birth).days // 365
                if age < 18:
                    error_r.value = "You must be at least 18 years old"
                    page.update()
                    return
            except Exception:
                error_r.value = "Invalid date format (use dd.mm.yyyy)"
                page.update()
                return

            page.snack_bar = ft.SnackBar(ft.Text("Account created"), open=True)
            page.go("/login")

        page.update()

    register_btn = ft.ElevatedButton(
        text="Register",
        width=260,
        on_click=register,
    )

    back_btn = ft.TextButton(
        text="Back to login",
        on_click=lambda e: page.go("/login"),
    )

    card_r = ft.Card(
        content=ft.Container(
            padding=20,
            width=320,
            content=ft.Column(
                [
                    ft.Text("Create account", size=20, weight=ft.FontWeight.BOLD),
                    name,
                    email_r,
                    password_r,
                    confirm_r,
                    gender,
                    dob,
                    error_r,
                    register_btn,
                    back_btn,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                tight=True,
            ),
        ),
    )

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.GREY_100,
        content=card_r,
    )


def main(page: ft.Page):
    page.title = "Login / Register"

    def route_change(e: ft.RouteChangeEvent):
        page.controls.clear()
        if page.route == "/" or page.route == "/login":
            page.add(login_page(page))
        elif page.route == "/register":
            page.add(register_page(page))
        else:
            page.add(login_page(page))
        page.update()

    page.on_route_change = route_change
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)

import click
import api
import auth_helper


def login():
    id_token, refresh_token, uid = api.authenticate_user()
    if id_token and refresh_token:
        auth_helper.save_tokens(id_token, refresh_token, uid)
        click.echo("Logged in successfully.")
    else:
        click.echo("Login failed.")
    return id_token, refresh_token, uid


def logout():
    auth_helper.delete_data()
    click.echo("Logged out successfully.")


def validate_auth():
    id_token, refresh_token, uid = auth_helper.load_tokens()
    # print(id_token)

    if id_token is None or not api.is_token_valid(id_token):
        if refresh_token:
            new_id_token, new_refresh_token, uid = api.refresh_id_token(refresh_token)
            if new_id_token and new_refresh_token:
                auth_helper.save_tokens(new_id_token, new_refresh_token, uid)
                return new_id_token, new_refresh_token, uid
        click.echo("No valid token or refresh token")
        return None, None, None
    return id_token, refresh_token, uid

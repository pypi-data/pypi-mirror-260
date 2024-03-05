from fastapi import HTTPException, Header

from komodo.framework.komodo_app import KomodoApp
from komodo.loaders.user_loader import UserLoader

g_appliance: KomodoApp = KomodoApp(name="Placeholder", shortcode="placeholder",
                                   purpose="Placeholder")  # Replace with the actual appliance object


def get_appliance():
    if not g_appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    return g_appliance


def set_appliance_for_fastapi(appliance):
    global g_appliance
    g_appliance = appliance


def get_email_from_header(x_user_email: str = Header(None)):
    if x_user_email is None:
        raise HTTPException(status_code=400, detail="X-User-Email header missing")

    print("X-User-Email: ", x_user_email)
    try:
        user = UserLoader.load(x_user_email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found: " + x_user_email)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Can not validate: " + x_user_email + " - " + str(e))
    return x_user_email

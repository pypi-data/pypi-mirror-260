"""Database management functions for the Palworld Admin API."""

import logging

from sqlalchemy.exc import SQLAlchemyError

from palworld_admin.classes.dbmodels import db, LauncherSettings, Connection


def get_stored_default_settings(model_name: str) -> dict:
    """
    Returns the stored information for the first row of the specified model.

    Parameters:
    - model_name: The name of the model to return information for ("Connection" or "LauncherSettings").

    Returns:
    A dictionary with model fields as keys and their stored values as values.
    """
    if model_name == "Connection":
        model = Connection
    elif model_name == "LauncherSettings":
        model = LauncherSettings
    else:
        return {"error": f"Invalid model name: {model_name}"}

    record = model.query.first()
    if not record:
        return {"error": f"No records found for model: {model_name}"}

    # Dynamically build a dictionary of the record's columns and their values
    record_info = {
        column.name: getattr(record, column.name)
        for column in record.__table__.columns
    }
    return record_info


def update_object_fields(obj, data, fields) -> list:
    """
    Update fields of an object based on provided data.

    Parameters:
    - obj: The object to update.
    - data: A dictionary with new values.
    - fields: A list of fields to update.

    Returns:
    A list of updated field names.
    """
    ignored_fields = [
        "rcon_port",
        "public_port",
        "port",
        "public_ip",
    ]
    updated_fields = []
    for field in fields:
        if field in data:
            # if field is rcon_port, skip it
            if field in ignored_fields:
                continue
            if getattr(obj, field) != data[field]:
                setattr(obj, field, data[field])
                updated_fields.append(field)
    return updated_fields


def save_user_settings_to_db(user_settings) -> dict:
    """Save user settings to the database."""
    log = True
    result = {}

    if log:
        logging.info(
            "Saving user settings to the database:\n%s", user_settings
        )

    try:
        # Refactored LauncherOptions update
        if "launcher_options" in user_settings:
            # create a list of fields from the keys in the dictionary
            fields = list(user_settings["launcher_options"].keys())
            if log:
                logging.info("Fields: %s", fields)
            launcher_settings = user_settings["launcher_options"]
            launcher_options = LauncherSettings.query.get(1)
            if launcher_options:
                updated_fields = update_object_fields(
                    launcher_options,
                    launcher_settings,
                    fields,
                )
                if updated_fields:
                    db.session.commit()
                    result["launcher_options"] = "updated"

        # Refactored Connection update
        if "rcon_last_connection" in user_settings:
            connection_data = user_settings["rcon_last_connection"]
            if log:
                logging.info("Connection data: %s", connection_data)
            connection = Connection.query.first()
            if connection:
                updated_fields = update_object_fields(
                    connection, connection_data, ["host", "port", "password"]
                )
                if updated_fields:
                    db.session.commit()
                    result["rcon_last_connection"] = "updated"

        # Handle rcon_new_connection
        if "rcon_new_connection" in user_settings:
            new_connection_data = user_settings["rcon_new_connection"]
            connection = Connection.query.filter_by(
                host=new_connection_data["host"],
                port=new_connection_data["port"],
            ).first()

            if connection:
                updated_fields = update_object_fields(
                    connection, new_connection_data, ["password", "name"]
                )
                if updated_fields:
                    db.session.commit()
                    result["rcon_new_connection"] = (
                        f"updated: {' and '.join(updated_fields)}"
                    )
            else:
                new_connection = Connection(**new_connection_data)
                db.session.add(new_connection)
                db.session.commit()
                result["rcon_new_connection"] = "created"

        result["status"] = "success"

    except SQLAlchemyError as e:
        db.session.rollback()
        result["status"] = "error"
        result["error"] = str(e)
        logging.error("Error saving user settings to the database: %s", str(e))

    db.session.close()

    return result

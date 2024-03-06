# Copyright 2024 Louis Paternault
#
# This file is part of pdfimpose-web.
#
# Pdfimpose-web is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pdfimpose-web is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfimpose-web. If not, see <https://www.gnu.org/licenses/>.

"""Web interface to pdfimpose https://framagit.org/spalax/pdfimpose"""

import atexit
import contextlib
import datetime
import os
import pathlib
import secrets
import shutil
import tempfile
import time

import papersize
import pdfimpose
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_babel import Babel
from flask_babel import lazy_gettext as _
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from . import clean, database, layout, limiter, settings

VERSION = "1.0.0"


def allowed_file(filename: str):
    """Return `True` if the filename is allowed."""
    return filename.endswith(".pdf")


def papersizetranslations():
    """Return the location of translation of package `papersize`."""
    # Thanks to:
    # https://importlib-resources.readthedocs.io/en/latest/migration.html#pkg-resources-resource-filename
    file_manager = contextlib.ExitStack()
    atexit.register(file_manager.close)
    return file_manager.enter_context(papersize.translation_directory())


# pylint: disable=too-many-statements
def create_app():
    """Create and configure the application"""

    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.add_extension("jinja2.ext.loopcontrols")

    # Load options
    settings.set_configuration(app)

    app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

    # Configure Babel
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = (
        f"translations;{papersizetranslations()}"
    )
    app.config["BABEL_DOMAIN"] = "messages;papersize"

    def get_locale():
        return request.accept_languages.best_match(
            locale.language for locale in babel.list_translations()
        )

    babel = Babel(app, locale_selector=get_locale)

    # Configure database
    database.init(app)

    # Configure limiter
    limiter.init(app)

    # Create temporary folder
    app.config["TEMP_FOLDER"].mkdir(parents=True, exist_ok=True)

    # Clean files from older runs, and create cleaner (that removes PDFs)
    if app.config["RUN_CLEANER_THREAD"]:
        toremove = clean.launch_thread_cleaner(app)

    # Add stuff to template context

    @app.context_processor
    def context_processor():
        return {
            "UNITS": {
                key: _(value).split("(")[0].strip()
                for key, value in papersize.UNITS_HELP.items()
                if key in ("pt", "mm", "cm", "in")
            },
            "SIZES": {key: _(value) for key, value in papersize.SIZES_HELP.items()},
            "LAYOUTS": (
                "cards",
                "copycutfold",
                "cutstackfold",
                "hardcover",
                "onepagezine",
                "pdfautonup",
                "saddle",
                "wire",
            ),
            "lang": app.extensions["babel"].locale_selector(),
            "stat": database.stat(),
            "max_size": database.prettyprint_size(
                app.config["MAX_CONTENT_LENGTH"], round_func=round
            ),
        }

    # Quick and dirty statistics page
    basic_auth = BasicAuth(app)

    # Redirect while keeping query string
    def smart_redirect(location, *args, **kwargs):
        if request.query_string:
            return redirect(
                f"{location}?{request.query_string.decode()}", *args, **kwargs
            )
        return redirect(location, *args, **kwargs)

    # Define routes

    @app.route("/stats")
    @basic_auth.required
    def stats():
        return render_template(
            "stats.html",
            dataday=database.get_history("day", dateformat='"%Y-%m-%d"'),
            dataweek=database.get_history("week", dateformat='"%Y-%m-%d"'),
            datamonth=database.get_history("month", dateformat='"%Y-%m"'),
            datayear=database.get_history("year", dateformat='"%Y"'),
        )

    @app.route("/", methods=["GET", "POST"])
    def root():
        if request.method == "POST":
            # Catch argument errors
            try:
                if (
                    app.config["MAX_FILE_REPEAT"]
                    != 0  # MAX_FILE_REPEAT == 0 means no limit
                    and int(
                        request.form.to_dict()[
                            f"""form-{request.form["layout"]}-repeat"""
                        ]
                    )
                    > app.config["MAX_FILE_REPEAT"]
                ):
                    flash(
                        _("Error: The maximum number of repetitions is %s.", "impose")
                        % app.config["MAX_FILE_REPEAT"]
                    )
                    return smart_redirect("/")
            except (KeyError, ValueError):
                pass

            # Get raw list of (possibly bad) file names
            rawfiles = request.files.getlist("file")

            # Remove bad files, save good files
            tempdir = pathlib.Path(
                tempfile.mkdtemp(
                    prefix=datetime.datetime.now().strftime("%Y%m%d-%H%M%S-"),
                    dir=app.config["TEMP_FOLDER"],
                )
            )
            uploaddir = tempdir / "upload"
            uploaddir.mkdir(parents=True, exist_ok=True)

            sourcefiles = []
            totalsize = 0
            for file in rawfiles:
                if not file.filename:
                    flash(_("Error: No file."), "files")
                    continue
                if not allowed_file(file.filename):
                    flash(_("Error: Invalid filename."), "files")
                    continue
                sourcefiles.append(pathlib.Path(secure_filename(file.filename)))
                file.save(uploaddir / sourcefiles[-1])
                totalsize += (uploaddir / sourcefiles[-1]).stat().st_size

            # No source files…
            if not sourcefiles:
                flash(
                    _("No valid PDF files found. Try uploading a valid PDF file."),
                    "files",
                )
                return smart_redirect("/")

            # Create download directory
            downloaddir = tempdir / "download"
            downloaddir.mkdir(parents=True, exist_ok=True)
            destfile = f"{sourcefiles[0].stem}-impose{sourcefiles[0].suffix}"

            # Impose file
            try:
                layout.impose(
                    request.form["layout"],
                    infile=uploaddir / sourcefiles[0],
                    outfile=downloaddir / destfile,
                    arguments=request.form.to_dict(),
                )
            except pdfimpose.UserError as error:
                flash(  #  pylint: disable=consider-using-f-string
                    _("Error while imposing files: %s", "impose") % error
                )
                return smart_redirect("/")

            # Imposition succeeded. Log it in the database
            database.add(totalsize)

            # Remove source files, and mark produced file for removal
            shutil.rmtree(uploaddir, ignore_errors=True)
            if app.config["RUN_CLEANER_THREAD"]:
                toremove.put(
                    (datetime.datetime.now() + app.config["PDF_LIFETIME"], tempdir)
                )

            # Everything went right!
            return send_from_directory(
                downloaddir,
                destfile,
                as_attachment=True,
            )
        # Method POST (or anything but GET)
        if "noscript" in request.args:
            return render_template("noscript.html")
        return render_template(
            "index.html",
        )

    @app.errorhandler(413)
    def error413(error):
        #  pylint: disable=unused-argument
        flash(
            _(
                "Error: File is too big: maximum size is %s.",
            )
            % database.prettyprint_size(
                app.config["MAX_CONTENT_LENGTH"], round_func=round
            ),
            "files",
        )
        return render_template("index.html"), 413

    return app

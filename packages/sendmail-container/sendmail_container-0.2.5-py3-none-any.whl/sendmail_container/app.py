from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from pydantic import NameEmail
from pydantic_settings import BaseSettings
from starlette.responses import PlainTextResponse


class EnvConfig(BaseSettings):
    email_host: str = "localhost"
    email_host_uri: str = "127.0.0.1"

    class Config:
        env_file = ".env"


envconfig = EnvConfig()
app = FastAPI()


@app.exception_handler(HTTPException)
def inform_error(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.post("/sendmail/")
def sendmail(
    sender_prefix: Optional[str] = Form("maildaemon"),
    email_server_alias: Optional[str] = Form(envconfig.email_host),
    recipients: List[NameEmail] = Form(...),
    mail_title: Optional[str] = Form("(Empty Subject)"),
    mail_body: Optional[str] = Form(None),
    attachments: List[UploadFile] = File(None),
):
    try:
        with SMTP(envconfig.email_host_uri) as server:
            message = MIMEMultipart("mixed")
            message["From"] = f"{sender_prefix}@{email_server_alias}"
            message["To"] = ",".join(list(map(lambda x: x.email, recipients)))
            message["Subject"] = mail_title
            if mail_body:
                message.attach(MIMEText(mail_body, "html"))
            if attachments:
                for attachment in attachments:
                    file_attachment = MIMEApplication(attachment.file.read())
                    file_attachment.add_header(
                        "Content-Disposition", "attachment", filename=attachment.filename
                    )
                    message.attach(file_attachment)
            server.connect()
            server.sendmail(
                from_addr=f"{sender_prefix}@{email_server_alias}",
                to_addrs=list(map(lambda x: x.email, recipients)),
                msg=message.as_string(),
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e.__class__.__name__}: {e}")

    return Response("Success!", status_code=200)

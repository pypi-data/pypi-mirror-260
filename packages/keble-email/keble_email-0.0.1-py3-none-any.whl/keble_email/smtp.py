from datetime import datetime
from typing import Any, Dict, List, Optional
import jinja2
import mjml
from pathlib import Path
import emails
from emails.template import JinjaTemplate
from .schemas import EmailSettingABC
from emails.backend.response import SMTPResponse


class EmailSender:
    @classmethod
    def use_template(cls,
                     mjml_template: Optional[str | Path] = None,
                     html_template: Optional[str | Path] = None,
                     environment: Optional[Dict[str, Any]] = None) -> str:
        assert html_template is not None or mjml_template is not None
        assert html_template is None or mjml_template is None
        jinja_env = jinja2.Environment()
        if html_template is not None:
            with open(html_template) as f:
                template_str = f.read()
        else:
            with open(mjml_template) as f:
                template_str = f.read()
        compiled_template = jinja_env.from_string(template_str)
        _output = compiled_template.render(environment)
        if html_template is not None:
            return _output
        else:
            return mjml.mjml_to_html(_output).html

    @classmethod
    def _send_with_smtp(cls, *,
                        subject: str,
                        recipient_email: str,
                        sender_email: str,
                        sender_name: str,
                        smtp_user: str,
                        smtp_password: str,
                        smtp_host: str,
                        smtp_port: int,
                        smtp_tls: bool,
                        smtp_ssl: bool,
                        html: str,
                        cc: Optional[str] = None,
                        bcc: Optional[str] = None,
                        attachment_path: Optional[str] = None):
        smtp_options = {"host": smtp_host, "port": smtp_port}
        if smtp_tls:
            smtp_options["tls"] = True
        if smtp_ssl:
            smtp_options["ssl"] = True
        if smtp_user:
            smtp_options["user"] = smtp_user
        if smtp_password:
            smtp_options["password"] = smtp_password
        message = emails.Message(
            subject=JinjaTemplate(subject),
            html=JinjaTemplate(html),
            mail_from=(sender_name, sender_email),
            cc=cc,
            bcc=bcc
        )

        if attachment_path is not None:
            with open(attachment_path, "rb") as f:
                message.attach(data=f.read(), filename=attachment_path.split("/")[-1])

        res: SMTPResponse = message.send(to=recipient_email, smtp=smtp_options)

        return {
            "status_code": res.status_code,
            "success": res.success,
            "smtp_host": smtp_host,
            "html": message.html.template_text,
            "text": message.text,
            "sender_name": sender_name,
            "sender_email": sender_email,
            "email_to": recipient_email,
            "time": datetime.utcnow()
        }

    @classmethod
    def send(cls, *,
             mjml_template: Optional[str] = None,
             html_template: Optional[str] = None,
             html: Optional[str] = None,
             environment: Optional[Dict[str, Any]] = None,
             settings: Optional[EmailSettingABC] = None,
             sender_email: Optional[str] = None,
             sender_name: Optional[str] = None,
             smtp_user: Optional[str] = None,
             smtp_password: Optional[str] = None,
             smtp_host: Optional[str] = None,
             smtp_port: Optional[int] = None,
             smtp_tls: Optional[bool] = None,
             smtp_ssl: Optional[bool] = None,
             **kwargs
             ):
        environment = environment if environment is not None else {}
        if html is None:
            html = cls.use_template(mjml_template, html_template, environment)

        return cls._send_with_smtp(html=html,
                                   sender_email=settings.sender_email if settings is not None else sender_email,
                                   sender_name=settings.sender_name if settings is not None else sender_name,
                                   smtp_user=settings.smtp_user if settings is not None else smtp_user,
                                   smtp_password=settings.smtp_password if settings is not None else smtp_password,
                                   smtp_host=settings.smtp_host if settings is not None else smtp_host,
                                   smtp_port=settings.smtp_port if settings is not None else smtp_port,
                                   smtp_tls=settings.smtp_tls if settings is not None else smtp_tls,
                                   smtp_ssl=settings.smtp_ssl if settings is not None else smtp_ssl,
                                   **kwargs)

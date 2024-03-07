import base64
from warnings import warn
from typing import TypeVar, TypedDict, Union
from typing_extensions import Unpack

SelfMailParams = TypeVar("SelfMailParams", bound="MailParams")


class AttachmentParams(TypedDict):
    content: str
    disposition: str
    id: Union[str, None]
    filename: Union[str, None]


class MailParamsParams(TypedDict):
    from_email: Union[str, None]
    from_name: Union[str, None]
    to_email: Union[str, None]
    to_name: Union[str, None]
    subject: Union[str, None]
    reply_to: Union[str, None]
    preview_text: Union[str, None]
    template_id: Union[str, None]
    text: Union[str, None]
    html: Union[str, None]
    substitutions: Union[dict, None]
    context: Union[dict, None]
    attachments: Union[list, None]
    variables: Union[dict, None]


class Attachment():

    INLINE = 'inline'
    ATTACHMENT = 'attachment'

    def __init__(self, **kwargs: Unpack[AttachmentParams]):
        self.content = kwargs.get('content')
        self.disposition = kwargs.get('disposition')
        self.id = kwargs.get('id', None)
        self.filename = kwargs.get('filename', None)

        if self.disposition not in [self.INLINE, self.ATTACHMENT]:
            raise ValueError(f'Invalid disposition {self.disposition}')

        if self.disposition == self.ATTACHMENT:
            if self.filename is None:
                raise ValueError(
                    'Parameter filename is required when '
                    'disposition is attachment')
        elif self.disposition == self.INLINE:
            if self.id is None:
                raise ValueError(
                    'Parameter id is required when '
                    'disposition is inline')

        if not self.is_base64(self.content):
            self.content = base64.b64encode(self.content).decode('utf-8')

    def is_base64(self, s: str) -> bool:
        try:
            return base64.b64encode(
                base64.standard_b64decode(s)).decode('utf-8') == s
        except Exception:
            return False

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'filename': self.filename,
            'disposition': self.disposition,
            'content': self.content
        }


class MailParams():

    def __init__(self, **kwargs: Unpack[MailParamsParams]):
        self.from_email = kwargs.get('from_email', None)
        self.from_name = kwargs.get('from_name', None)
        self.to_email = kwargs.get('to_email', None)
        self.to_name = kwargs.get('to_name', None)
        self.subject = kwargs.get('subject', None)
        self.reply_to = kwargs.get('reply_to', None)
        self.preview_text = kwargs.get('preview_text', None)
        self.template_id = kwargs.get('template_id', None)
        self.text = kwargs.get('text', None)
        self.html = kwargs.get('html', None)
        self.substitutions = kwargs.get('substitutions', {})
        self.context = kwargs.get('context', {})
        self.attachments = kwargs.get('attachments', [])
        self.variables = kwargs.get('variables', {})

    def setTo(self,
              to_email: str,
              to_name: Union[str, None]) -> SelfMailParams:
        self.to_email = to_email
        self.to_name = to_name
        return self

    def setFrom(self,
                from_email: str,
                from_name: Union[str, None]) -> SelfMailParams:
        self.from_email = from_email
        self.from_name = from_name
        return self

    def setSubject(self, subject: str) -> SelfMailParams:
        self.subject = subject
        return self

    def setPreviewText(self, preview_text: str) -> SelfMailParams:
        self.preview_text = preview_text
        return self

    def setReplyTo(self, reply_to: str) -> SelfMailParams:
        self.reply_to = reply_to
        return self

    def setTemplateID(self, template_id: str) -> SelfMailParams:
        self.template_id = template_id
        return self

    def setHTML(self, html: str) -> SelfMailParams:
        self.html = html
        return self

    def setText(self, text: str) -> SelfMailParams:
        self.text = text
        return self

    def setVariables(self, variables: dict) -> SelfMailParams:
        self.variables = variables

    def setSubstitutions(self, substitutions: dict) -> SelfMailParams:
        warn('This method is deprecated. Use setContext() instead.',
             DeprecationWarning)
        self.substitutions = substitutions
        return self

    def setContext(self, context: dict) -> SelfMailParams:
        self.context = context
        return self

    def addAttachment(self, attachment: Attachment) -> SelfMailParams:
        self.attachments.append(attachment)
        return self

    def is_scalar(self, value) -> bool:
        return type(value) in [bool, str, float, int]

    def to_dict(self) -> dict:
        """
        Converts the object attributes into a dictionary
        that has the same structure as the required JSON
        """
        # Integrity Checks
        if self.to_email is None:
            raise ValueError('Email address "To" must be set')

        if self.template_id is None and \
           (self.html is None and self.text is None):
            raise ValueError('No content (html nor text) was provided. '
                             'Please set either the text or html attributes, '
                             'or specify a template ID')

        if self.template_id is not None and \
           (self.html is not None or self.text is not None):
            raise ValueError('Content (html or text) and templates '
                             'are mutually exclusive')

        if self.template_id is None:
            if self.from_email is None:
                raise ValueError('Email address "From" must be set')

            if self.subject is None:
                raise ValueError('Subject must be set')

        for substitution in self.substitutions.values():
            if not self.is_scalar(substitution):
                raise ValueError('Substitutions can only be scalar values')

        # Copy substitutions to context if necessary
        if len(self.substitutions.items()) > 0 and \
           len(self.context.items()) == 0:
            self.context = self.substitutions

        result = {}

        # Pass only email if no name was provided
        if self.from_name is None:
            result['from'] = self.from_email
        else:
            result['from'] = {
                'email': self.from_email,
                'name': self.from_name
            }

        # Pass only email if no name was provided
        if self.to_name is None:
            result['to'] = self.to_email
        else:
            result['to'] = {
                'email': self.to_email,
                'name': self.to_name
            }

        if self.subject is not None:
            result['subject'] = self.subject

        if self.reply_to is not None:
            result['reply_to'] = self.reply_to

        if self.preview_text is not None:
            result['preview_text'] = self.preview_text

        # Pass only needed keys
        if self.template_id is not None:
            result['templateID'] = self.template_id
        else:
            if self.text is not None:
                result['text'] = self.text
            if self.html is not None:
                result['html'] = self.html

        # Add remaining keys
        result['context'] = self.context
        result['variables'] = self.variables

        # Serialize attachments
        result['attachments'] = \
            [attachment.to_dict() for attachment in self.attachments]

        return result

import io

from ormspace import functions
from ormspace.bases import ModelType
from ormspace.enum import Gender
from ormspace.model import getmodel
from starlette.requests import Request

from detadoc.bases import Profile
from detadoc.models import Patient

class Element(str):
    def __new__(cls, tag, content="", klass="", config=""):
        new = super().__new__(cls)
        new.tag = tag
        new.content = content
        new.klass = klass
        new.config = config
        return new
    
    def __str__(self):
        with io.StringIO() as buf:
            buf.write(f'<{self.tag}')
            if self.klass:
                buf.write(f' class="{self.klass}"')
            if self.config:
                buf.write(f' {self.config}')
            buf.write('>')
            if self.content:
                buf.write(self.content)
            buf.write(f'</{self.tag}>')
            return buf.getvalue()

def ul(content: str, klass: str = "list-group list-group-flush", config: str = "") -> str:
    return Element('ul', content=content, klass=klass, config=config)

def li(content: str, klass: str = "list-group-item", config: str = "") -> str:
    return Element('li', content=content, klass=klass, config=config)

def a(content: str, klass: str = "list-group-item-action", config: str = "") -> str:
    return Element('a', content=content, klass=klass, config=config)

def div(content: str, klass: str = "container", config: str = "") -> str:
    return Element('div', content=content, klass=klass, config=config)


async def session_user(request: Request):
    if user:= request.session.get('user'):
        model = getmodel(user.get("table"))
        return model(**user)
    return None

async def get_patient(request: Request):
    return await Patient.fetch_instance(
            request.path_params.get('patient_key', request.query_params.get('patient_key'))
    )

def greetings(profile: Profile = None):
    now = functions.now()
    hour = now.hour
    start = 'Bom dia!' if hour < 12 else 'Boa tarde!' if hour < 18 else 'Boa noite!'
    if not profile:
        return start
    final = f'Seja bem vinda {profile.fname}!' if profile.gender.name == 'Female' else f'Seja bem vindo {profile.fname}!'
    return f'{start} {final}'

    
    


if __name__ == '__main__':
    
    x = div( 'Daniel')
    print(x)
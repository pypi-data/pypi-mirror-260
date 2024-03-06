from __future__ import annotations

import calendar
import datetime
import io
from decimal import Decimal
from io import StringIO
from typing import Annotated, Any, ClassVar, NamedTuple, Optional, Union

import bcrypt
from markdown import markdown
from markupsafe import Markup
from ormspace import functions
from ormspace.enum import StrEnum
from ormspace.functions import string_to_list
from spacestar.model import SpaceModel
from ormspace.model import getmodel, modelmap, SearchModel
from ormspace.annotations import DateField, DateTimeField, ListOfStrings, OptionalDate, OptionalFloat, PasswordField, \
    PositiveDecimalField, \
    PositiveIntegerField
from pydantic import BaseModel, BeforeValidator, computed_field, Field, RootModel
from starlette.requests import Request
from typing_extensions import Self

from detadoc.annotations import BodyMeasureFloat, BodyMeasureInteger, OptionalBoolean
from detadoc.bases import EmailBase, FinancialBase, Profile, SpaceSearchModel, Staff, Transaction
from detadoc.enum import Account, AccountSubtype, CashFlow, enummap, \
    Frequency, \
    Intensity, \
    InvoiceType, AccountType, \
    DosageForm, \
    Kinship, Level, MedicationRoute, \
    Month, PaymentMethod, Period, Quality, Recurrence, DayTime
from detadoc.regex import ActiveDrug, Package, ProfileMessage


@modelmap
class User(EmailBase):
    TABLE_NAME = 'User'
    EXIST_QUERY = 'email'
    password: PasswordField
    created: DateField
    updated: Optional[datetime.date] = Field(None)
    profile_tablekey: str
    profile: Union[Doctor, Employee, Patient, None] = Field(None, init_var=False)
    
    def __str__(self):
        return self.email
    
    @property
    def profile_table(self):
        return self.profile_tablekey.split('.')[0]
    
    async def setup_request_session(self, request: Request) -> Request:
        await self.setup_instance()
        try:
            admin = await Doctor.admin_instance()
            if admin:
                request.session['admin'] = str(admin)
        finally:
            pass
        request.session['user'] = self.profile.asjson()
        request.session['user']['table'] = self.profile.table()
        if self.profile_tablekey == 'Doctor.admin':
            request.session['is_admin'] = True
        else:
            request.session['is_admin'] = False
        return request
    
    
    @property
    def profile_key(self):
        return self.profile_tablekey.split('.')[-1]
    
    async def setup_instance(self):
        if not self.profile:
            self.profile = await getmodel(self.profile_table).fetch_instance(self.profile_key)
    
    @classmethod
    async def get_and_check(cls, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(email)
        if user:
            if user.check(password):
                return user
        return None
    
    @classmethod
    def create_encrypted(cls, email: str, password: str) -> Self:
        return cls(email=email, password=cls.encrypt_password(password))
    
    @classmethod
    def encrypt_password(cls, password: str) -> bytes:
        return bcrypt.hashpw(functions.str_to_bytes(password), bcrypt.gensalt())
    
    def check(self, password: str) -> bool:
        return bcrypt.checkpw(functions.str_to_bytes(password), self.password)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.email == other.email
    
    def __hash__(self):
        return hash(self.email)


@modelmap
class Register(User):
    TABLE_NAME = 'User'
    password_repeat: bytes
    
    def model_post_init(self, __context: Any) -> None:
        assert self.password == self.password_repeat
        self.password = self.encrypt_password(self.password)
    
    def asjson(self):
        data = super().asjson()
        data.pop('password_repeat', None)
        return data
    

@modelmap
class Patient(Profile):
    MODEL_GROUPS = ['Profile']
    
def just_date(value: str) -> str:
    if isinstance(value, str):
        if len(value) > 10:
            return value[:10]
    return value

class CreatedBase(SpaceModel):
    created: Annotated[DateField, BeforeValidator(just_date)] = Field(title='Data da Criação')
    
    def __lt__(self, other):
        return self.created < other.created
    
    @property
    def past_days(self) -> int:
        return (datetime.date.today() - self.created).days
    
    
class PactientKeyBase(CreatedBase):
    EXIST_QUERY = 'created daytime patient_key'
    patient_key: Patient.Key = Field(title='Chave do Paciente')
    daytime: DayTime = Field(DayTime.T12_00, title='Hora da Criação')

    
    def __lt__(self, other):
        return self.created < other.created

    
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if self.patient_key:
            if not self.patient_key.instance:
                if patient:= Patient.instance_from_context(self.patient_key.key):
                    self.patient = patient
                    
    @property
    def patient(self) -> Patient:
        return self.patient_key.instance if self.patient_key else None
    
    @patient.setter
    def patient(self, value: Patient) -> None:
        self.patient_key.set_instance(value)


class MentalExamBase(PactientKeyBase):
    notes: Optional[str] = None

@modelmap
class Symptom(PactientKeyBase):
    SINGULAR = 'Sintoma'
    date: DateField
    intensity: Intensity = Intensity.I3
    recurrence: Recurrence = Recurrence.U
    name: str
    
    def __str__(self):
        if self.past_days > 2:
            return f'{self.name} (há {self.past_days} dias)'
        return f'{self.name}'


class ProfessionalBase(Staff):
    graduation_year: int
    graduation_university: str
    specialties: ListOfStrings
    subspecialties: ListOfStrings


@modelmap
class Doctor(ProfessionalBase):
    MODEL_GROUPS = ['Profile', 'Staff']
    EXIST_QUERY = 'key'
    crm: Optional[str] = None

    @classmethod
    async def admin_data(cls) -> dict:
        return await cls.fetch_one('admin')
    
    @classmethod
    async def admin_instance(cls) -> Optional[Self]:
        if data := await cls.admin_data():
            return cls(**data)
        return None
    
    def __str__(self):
        if self.gender.value.lower().startswith('masculino'):
            return f'Dr. {self.name}'
        return f'Dra. {self.name}'
    
    
@enummap
class Admin(Doctor):
    TABLE_NAME = 'Doctor'
    
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self.key = 'admin'


@modelmap
class Employee(Staff):
    MODEL_GROUPS = ['Profile', 'Staff']


@modelmap
class Service(SearchModel):
    FETCH_QUERY = {'active': True}
    name: str
    price: PositiveDecimalField
    return_days: PositiveIntegerField = Field(0)
    active: bool = Field(True)
    notes: ListOfStrings
    created: DateField
    
    def __str__(self):
        return f'{self.name} valor R$ {self.price}'
    
    
# FINANCIAL

@modelmap
class JournalEntry(SpaceModel):
    transaction: Transaction
    description: str = ''
    
    def __lt__(self, other):
        assert isinstance(other, type(self))
        return self.transaction.accounting_date < other.transaction.accounting_date
    
    def __str__(self):
        return f'{self.transaction.display} {self.description}'
    
    @property
    def value(self) -> Decimal:
        if self.account.type == self.transaction_type:
            return self.amount
        return Decimal('0') - self.amount
    
    @property
    def account(self):
        return self.transaction.account
    
    @property
    def amount(self):
        return self.transaction.amount
    
    @property
    def account_subtype(self):
        return self.account.subtype
    
    @property
    def account_type(self):
        return self.account.subtype.type
    
    @property
    def transaction_type(self):
        return self.transaction.type
    
    @property
    def date(self) -> datetime.date:
        return self.transaction.accounting_date
    
    def balance(self):
        return sum([i.amount for i in self.assets()]) - sum([i.amount for i in self.liabilities()]) - sum(
                i.amount for i in self.equity())
    
    def revenues(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.RE]
    
    def expenses(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.EX]
    
    def assets(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.AT]
    
    def liabilities(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.LI]
    
    def equity(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.SE]
    
    def dividends(self):
        return [i for i in self.transactions if i.account.type == AccountSubtype.DI]
    
    def profit(self):
        return sum([i.amount for i in self.revenues()]) - sum([i.amount for i in self.expenses()])

@modelmap
class Invoice(FinancialBase):
    REVENUE_ACCOUNT: ClassVar[Account] = Account.GRE
    EXPENSE_ACCOUNT: ClassVar[Account] = Account.GEX
    PAYABLE_ACCOUNT: ClassVar[Account] = Account.PLI
    RECEIVABLE_ACCOUNT: ClassVar[Account] = Account.RAT
    CASH_ACCOUNT: ClassVar[Account] = Account.CAT
    BANK_ACCOUNT: ClassVar[Account] = Account.BAT
    DIVIDEND_ACCOUNT: ClassVar[Account] = Account.WDI
    INVOICE_TYPE: ClassVar[InvoiceType] = InvoiceType.G
    
    
    @computed_field
    @property
    def type(self) -> str:
        return self.INVOICE_TYPE.name
    
    def __str__(self):
        if self.flow == CashFlow.EX:
            if self.has_payment():
                return f'- {self.amount} R$ {self.date} {self.EXPENSE_ACCOUNT.title} {self.description}'
            return f'{self.amount} R$ {self.date + datetime.timedelta(days=31)} {self.PAYABLE_ACCOUNT.title} {self.description}'
        if self.has_payment():
            return f'{self.amount} R$ {self.date} {self.REVENUE_ACCOUNT.title} {self.description}'
        return f'{self.amount} R$ {self.date + datetime.timedelta(days=31)} {self.RECEIVABLE_ACCOUNT.title} {self.description}'
    
    def has_payment(self):
        return self.method != PaymentMethod.NO
    
    async def setup_instance(self):
        pass
    
    def not_same_day(self):
        return self.created != self.date
    
    @classmethod
    async def save_journal_entry(cls, data: dict):
        instance = cls(**data)
        await instance.setup_instance()
        transactions = []
        if instance.type == 'A':
            if instance.has_payment():
                assert instance.flow == CashFlow.RE
                transactions.append(f'{Account.RAT} {instance.amount} C {instance.date} {instance.key} {instance.description}')
                if instance.method == PaymentMethod.CA:
                    transactions.append(f'{instance.CASH_ACCOUNT} {instance.amount} D {instance.date} {instance.key} {instance.description}')
                elif instance.method in [PaymentMethod.PI, PaymentMethod.TR, PaymentMethod.DC, PaymentMethod.AD, PaymentMethod.CH, PaymentMethod.CC]:
                    transactions.append(f'{instance.BANK_ACCOUNT} {instance.amount} D {instance.date} {instance.key} {instance.description}')
            else:
                raise ValueError('Contas a receber somente podem ser recebidas.')
        elif instance.type == 'D':
            if instance.has_payment():
                assert instance.flow == CashFlow.EX
                transactions.append(f'{Account.WDI} {instance.amount} D {instance.date} {instance.key} {instance.description}')
                if instance.method == PaymentMethod.CA:
                    transactions.append(f'{instance.CASH_ACCOUNT} {instance.amount} C {instance.date} {instance.key} {instance.description}')
                elif instance.method in [PaymentMethod.PI, PaymentMethod.TR, PaymentMethod.DC, PaymentMethod.AD, PaymentMethod.CH, PaymentMethod.CC]:
                    transactions.append(f'{instance.BANK_ACCOUNT} {instance.amount} C {instance.date} {instance.key} {instance.description}')
            else:
                raise ValueError('Dividendos somente podem ser pagos.')
        elif instance.type == 'B':
            if instance.has_payment():
                assert instance.flow == CashFlow.EX
                transactions.append(f'{Account.PLI} {instance.amount} D {instance.date} {instance.key} {instance.description}')
                if instance.method == PaymentMethod.CA:
                    transactions.append(f'{instance.CASH_ACCOUNT} {instance.amount} C {instance.date} {instance.key} {instance.description}')
                elif instance.method in [PaymentMethod.PI, PaymentMethod.TR, PaymentMethod.DC, PaymentMethod.AD, PaymentMethod.CH, PaymentMethod.CC]:
                    transactions.append(f'{instance.BANK_ACCOUNT} {instance.amount} C {instance.date} {instance.key} {instance.description}')
            else:
                raise ValueError('Contas a pagar somente podem ser pagas.')
        else:
            account = instance.REVENUE_ACCOUNT if instance.flow == CashFlow.RE else instance.EXPENSE_ACCOUNT
            opposite_flow = "D" if account.type == AccountType.C else "C"
            if instance.has_payment():
                transactions.append(f'{account} {instance.amount} {account.type} {instance.date} {instance.key} {instance.description}')
                if instance.method == PaymentMethod.CA:
                    transactions.append(f'{instance.CASH_ACCOUNT} {instance.amount} {opposite_flow} {instance.date} {instance.key} {instance.description}')
                elif instance.method in [PaymentMethod.PI, PaymentMethod.TR, PaymentMethod.DC, PaymentMethod.AD, PaymentMethod.CH, PaymentMethod.CC]:
                    transactions.append(f'{instance.BANK_ACCOUNT} {instance.amount} {opposite_flow} {instance.date} {instance.key} {instance.description}')
            else:
                transactions.append(f'{account} {instance.amount} {account.type} {instance.created} {instance.key} {instance.description}')
                if instance.flow == CashFlow.RE:
                    transactions.append(f'{instance.RECEIVABLE_ACCOUNT} {instance.amount} {instance.RECEIVABLE_ACCOUNT.type} {instance.date} {instance.key} {instance.description}')
                else:
                    transactions.append(f'{instance.PAYABLE_ACCOUNT} {instance.amount} {instance.PAYABLE_ACCOUNT.type} {instance.date} {instance.key} {instance.description}')

        await JournalEntry.Database.put_all([i.asjson() for i in [JournalEntry(transaction=t, description=instance.description or str(instance)) for t in transactions]])

    
    async def save_new(self):
        new = await super().save_new()
        if new:
            await self.save_journal_entry(new)
        return new
    
    async def delete(self):
        entries = await JournalEntry.sorted_instances_list({'transaction?contains': self.key})
        for entry in entries:
            await entry.delete()
        return await super().delete()


@modelmap
class RentInvoice(Invoice):
    REVENUE_ACCOUNT = Account.RRE
    EXPENSE_ACCOUNT = Account.REX
    INVOICE_TYPE = InvoiceType.R
    TABLE_NAME = 'Invoice'

@modelmap
class ProductInvoice(Invoice):
    REVENUE_ACCOUNT = Account.PRE
    EXPENSE_ACCOUNT = Account.PEX
    INVOICE_TYPE = InvoiceType.P
    TABLE_NAME = 'Invoice'
    
@modelmap
class PatrimonialInvoice(Invoice):
    REVENUE_ACCOUNT = Account.PPE
    EXPENSE_ACCOUNT = Account.PPE
    INVOICE_TYPE = InvoiceType.T
    TABLE_NAME = 'Invoice'
    
    
@modelmap
class EarningsInvoice(Invoice):
    REVENUE_ACCOUNT = Account.REA
    EXPENSE_ACCOUNT = Account.REA
    INVOICE_TYPE = InvoiceType.E
    TABLE_NAME = 'Invoice'
    
@modelmap
class DividendInvoice(Invoice):
    INVOICE_TYPE = InvoiceType.D
    flow: CashFlow = CashFlow.EX
    TABLE_NAME: ClassVar[str] = 'Invoice'


@modelmap
class ServiceInvoice(Invoice, PactientKeyBase):
    REVENUE_ACCOUNT = Account.SRE
    EXPENSE_ACCOUNT = Account.SEX
    INVOICE_TYPE = InvoiceType.S
    TABLE_NAME = 'Invoice'
    service_key: Service.Key
    description: Optional[str] = Field('Receita de Serviço')
    discount: Annotated[
        PositiveDecimalField, Field(Decimal('0')), BeforeValidator(lambda x: Decimal('0') if not x else Decimal(x))]
    flow: CashFlow = CashFlow.RE

    def __str__(self):
        self.description = f'{self.service or self.service_key} {self.patient or self.patient_key}'
        return super().__str__()

    async def setup_instance(self):
        if not self.patient:
            self.patient_key.set_instance(await Patient.fetch_instance(self.patient_key.key))
        if not self.service:
            self.service_key.set_instance(await Service.fetch_instance(self.service_key.key))

    @property
    def service(self):
        return self.service_key.instance
    
    def balance(self):
        value = self.service.price - self.amount
        if value > self.discount:
            return value - self.discount
        return 0
    
    def ammount_check(self):
        return self.service.price - self.discount - self.amount
    

@modelmap
class ExpenseInvoice(Invoice):
    EXPENSE_ACCOUNT = Account.GEX
    INVOICE_TYPE = InvoiceType.G
    flow: CashFlow = CashFlow.EX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    

@modelmap
class EnergyInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.EEX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
@modelmap
class WaterInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.WEX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
@modelmap
class PhoneInvoice(ExpenseInvoice):
    EXPENSE_ACCOUNT = Account.TEX
    TABLE_NAME: ClassVar[str] = 'Invoice'


@modelmap
class RevenueInvoice(Invoice):
    REVENUE_ACCOUNT = Account.GRE
    INVOICE_TYPE = InvoiceType.G
    flow: CashFlow = CashFlow.RE
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
@modelmap
class DividendInvoice(Invoice):
    DIVIDEND_ACCOUNT = Account.WDI
    INVOICE_TYPE = InvoiceType.D
    flow: CashFlow = CashFlow.EX
    TABLE_NAME: ClassVar[str] = 'Invoice'
    
    
@modelmap
class ReceivableInvoice(Invoice):
    INVOICE_TYPE = InvoiceType.A
    
@modelmap
class PayableInvoice(Invoice):
    INVOICE_TYPE = InvoiceType.B
    
    
@modelmap
class Diagnosis(PactientKeyBase):
    FETCH_QUERY = {'end': None}
    EXIST_QUERY = 'created title'
    SINGULAR = 'Diagnóstico'
    title: str
    description: Optional[str] = None
    start: DateField
    end: OptionalDate
    
    async def setup_instance(self):
        pass
    
    def __str__(self):
        return f'{self.start.year} {self.title}'

    def __lt__(self, other):
        return self.start < other.start
    
    
    
@modelmap
class FamilyHistory(PactientKeyBase):
    SINGULAR = 'História Familiar'
    PLURAL = 'Histórias Familiares'
    kinship: Kinship
    title: str
    description: Optional[str] = None


@modelmap
class Medication(SpaceSearchModel):
    SINGULAR = 'Medicação'
    PLURAL = 'Medicações'
    EXIST_QUERY = 'search'
    label: Optional[str] = Field(None)
    drugs: Annotated[list[ActiveDrug], BeforeValidator(string_to_list)]
    route: MedicationRoute = Field(MedicationRoute.O)
    dosage_form: DosageForm
    package: Package
    pharmaceutical: Optional[str] = Field(None)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))
    
    @property
    def is_generic(self):
        return self.label in [None, '']
    
    @property
    def is_single_drug(self):
        return len(self.drugs) == 1
    
    @property
    def package_content(self):
        return getattr(self.package, '_content', None)
    
    @property
    def package_size(self):
        return Decimal(functions.parse_number(getattr(self.package, '_size', None)))

    @property
    def drug_names(self):
        return functions.join([getattr(i, '_name') for i in self.drugs], sep=" + ")
    
    @property
    def drug_strengths(self):
        return functions.join([f"{getattr(i, '_strength')}{getattr(i, '_unit')}" for i in self.drugs], sep=" + ")
    
    @property
    def name(self):
        if not self.is_generic:
            return f'{self.label} ({self.drug_names}) {self.drug_strengths}'
        return f'{self.drug_names.title()} {self.drug_strengths}'
    
    def __str__(self):
        return f'{self.name} {self.package}'


@modelmap
class Event(PactientKeyBase):
    SINGULAR = 'Evento'
    EXIST_QUERY = 'title date patient_key'
    title: str
    notes: Optional[str] = Field(None)
    date: OptionalDate
    age: OptionalFloat = Field(exclude=True)
    
        
    async def setup_instance(self):
        self.patient = await Patient.fetch_instance(self.patient_key.key)
        self.setup_event_date()
        
    def setup_event_date(self):
        if all([self.age, not self.date]):
            days = datetime.timedelta(days=functions.parse_number(self.age) * 365)
            dt = self.patient.bdate + days
            leap_days = calendar.leapdays(self.patient.bdate.year, dt.year)
            self.date = dt + datetime.timedelta(days=leap_days)
    
    def __lt__(self, other):
        return self.date < other.date
    
    
    def __str__(self):
        return f'{functions.years(self.date, self.patient.bdate)} anos: {self.title}'
    
    
@modelmap
class Report(PactientKeyBase):
    SINGULAR = 'Relatório'
    title: str = 'Relatório Médico'
    content: str
    
    def __str__(self):
        return f'{self.title} {self.created}'
    
    def markup(self):
        return Markup(markdown(f'''
# {self.title}
```{self.created.day} de {Month.read_int(self.created.month).value} de {self.created.year}```

{self.content}
'''))


@modelmap
class ExamResult(Report):
    SINGULAR = 'Resultado de Exame'
    
@modelmap
class LabResult(PactientKeyBase):
    SINGULAR = 'Resultado de Laboratório'
    data: dict = Field(default_factory=dict)

    
@modelmap
class Prescription(PactientKeyBase):
    SINGULAR = 'Prescrição'
    PLURAL = 'Prescrições'
    EXIST_QUERY = 'medication_key patient_key start'
    FETCH_QUERY = {'end': None}
    start: DateField
    medication_key: Medication.Key
    period: Period = Period.D1
    frequency: Frequency = Frequency.N1
    dosage: Decimal = Field(Decimal('1'))
    notes: Optional[str] = None
    duration: Decimal = Field(Decimal('30'))
    end: OptionalDate = None
    
    def __lt__(self, other):
        assert isinstance(other, type(self))
        return self.start < other.start
    
    def __str__(self):
        if self.end:
            return f'{self.medication.name}: {self.dosage} {self.medication.dosage_form.value.lower()} {self.frequency.value}/{self.period.value}  {self.notes or ""}. [{self.start} a {self.end}]'
        return f'{self.medication.name}: {self.dosage} {self.medication.dosage_form.value.lower()} {self.frequency.value}/{self.period.value}  {self.notes or ""}. [{self.remaining_days}/{self.duration} dias, {self.computed_boxes} cx]'
    
    # def asjson(self):
    #     data = super().asjson()
    #     data.pop('search', None)
    #     return data

    @property
    def medication(self):
        return self.medication_key.instance
    
    @property
    def computed_boxes(self) -> Optional[Decimal]:
        if self.duration:
            needed = self.duration * self.daily_dosage
            if package_size:= self.medication.package_size:
                return Decimal((needed/package_size).__ceil__())
        return Decimal('1')
    
    @property
    def daily_dosage(self):
        value = ((self.dosage * int(self.frequency))/self.period.days).__round__(2)
        if self.medication.dosage_form == DosageForm.DRO:
            day_needed = value / 20
        else:
            day_needed = value
        return day_needed
    
    @property
    def expiration_date(self) -> datetime.date:
        return self.start + datetime.timedelta(days=self.total_days.__float__())
    
    @property
    def total_days(self):
        return  ((self.computed_boxes * self.medication.package_size)/ self.daily_dosage).__round__(0)
    
    @property
    def remaining_days(self):
        today = datetime.date.today()
        if self.created <= today:
            return self.total_days - (datetime.date.today() - self.created).days
        return self.duration
    
    @medication.setter
    def medication(self, value: Medication):
        self.medication_key.set_instance(value)
        
    async def setup_instance(self):
        if not self.medication:
            self.medication = await Medication.fetch_instance(str(self.medication_key))
    
    
@modelmap
class PrescriptionStopped(Prescription):
    TABLE_NAME = 'Prescription'
    FETCH_QUERY = {'end?ne': None}
    
    
@modelmap
class Task(CreatedBase):
    TABLE_NAME = 'Task'
    creator: str 
    title: str
    description: str
    messages: list[ProfileMessage]
    

@modelmap
class PhysicalExam(PactientKeyBase):
    SINGULAR = 'Exame Físico'
    PLURAL = 'Exames Físicos'
    key: Optional[str] = Field(None, title='Chave')
    # created: DateField = Field(title='Criado em')
    weight: BodyMeasureFloat = Field(title='Peso (Kg)')
    height: BodyMeasureFloat = Field(title='Altura (cm)')
    waist: BodyMeasureFloat = Field(title='Cintura (cm)')
    hip: BodyMeasureFloat = Field(title='Quadril (cm)')
    sbp: BodyMeasureInteger = Field(title='PAS')
    dbp: BodyMeasureInteger = Field(title='PAD')
    hr: BodyMeasureInteger = Field(title='FC (bpm)')
    rr: BodyMeasureInteger = Field(title='FR (rpm)')
    notes: Optional[str] = None
    
    def __lt__(self, other):
        return self.created < other.created
    
    def __str__(self):
        with StringIO() as buf:
            buf.write(f'{self.created} {self.daytime.value}')
            for k, v in self.model_fields.items():
                if value := getattr(self, k):
                    if k == 'weight':
                        buf.write(f", peso {value}Kg")
                    elif k == 'height':
                        buf.write(f", altura {value}cm")
                    elif k == 'waist':
                        buf.write(f", cintura {value}cm")
                    elif k == 'hip':
                        buf.write(f", quadril {value}cm")
                    elif k == 'hr':
                        buf.write(f", FC {value}bpm")
                    elif k == 'rr':
                        buf.write(f", FR {value}rpm")
            if self.waist_hip_ratio:
                buf.write(f", CQR {self.waist_hip_ratio}")
            if self.bmi:
                buf.write(f", IMC {self.bmi}Kg/m2")
            if self.sbp and self.dbp:
                buf.write(f', PA {self.sbp}/{self.dbp}mmHg')
            return buf.getvalue()
    
    @property
    def waist_hip_ratio(self):
        if self.waist and self.hip:
            return (self.waist / self.hip).__round__(2)
        return None
    
    @property
    def bmi(self):
        if self.weight and self.height:
            return (self.weight / (self.height / 100 * self.height / 100)).__round__(1)
        return None
    

@modelmap
class MentalExam(PactientKeyBase):
    SINGULAR = 'Exame Mental'
    PLURAL = 'Exames Mentais'
    EXIST_QUERY = 'created patient_key time'

    time: DayTime = DayTime.T12_00
    @enummap
    class Aging(StrEnum):
        I = 'Indefinido'
        O = 'Envelhecido para a idade'
        R = 'Idade cronológica e aparente equivalentes'
        Y = 'Jovem para a idade'
        
    aging: Aging = Aging.I
    
    grooming: Quality = Field(Quality.Q2, title='aparação')
    hygiene: Quality = Field(Quality.Q2, title='higiene')
    clothing: Quality = Field(Quality.Q2, title='vestimenta')
    self_harm: Intensity = Field(Intensity.I0, title='automutilação')
    lesions: Intensity = Field(Intensity.I0, title='lesões')
    appearance_notes: Optional[str] = Field(None, title='notas de aparência')
    @enummap
    class EyeContact(StrEnum):
        I = 'Indefinido'
        L = 'Contato Visual Reduzido'
        R = 'Contato Visual Regular'
        H = 'Contato Visual Intenso'
        F = 'Olhar Fixo'
    
    @enummap
    class Engagement(StrEnum):
        I = 'Indefinido'
        T = 'Recusa falar'
        L = 'Pouco Cooperativo'
        R = 'Cooperativo'
        H = 'Muito Cooperativo'
    
    @enummap
    class FacialExpression(StrEnum):
        I = 'Indefinido'
        R = 'Expressão Relaxada'
        H = 'Expressão de Alegria'
        L = 'Expressão de Tristeza'
        A = 'Expressão De Raiva'
        D = 'Expressão Apática'
        F = 'Expressão De Medo'
        T = 'Expressão De Tensão'
        G = 'Expressão Rígida'
        C = 'Expressão Cabisbaixa'
        M = 'Expressão Tímida'
    
    @enummap
    class PsychomotorSpeed(StrEnum):
        I = 'Indefinido'
        L = 'Reduzida'
        R = 'Normal'
        H = 'Aumentada'
        
    psychomotor_speed: PsychomotorSpeed = Field(PsychomotorSpeed.I, title='velocidade psicomotora')
    @enummap
    class PsychomotorTonus(StrEnum):
        I = 'Indefinido'
        L = 'Reduzida'
        R = 'Normal'
        H = 'Aumentada'
    
    psychomotor_tonus: PsychomotorTonus = Field(PsychomotorTonus.I, title='tônus psicomotor')
    
    @enummap
    class PsychomotorCoordenation(StrEnum):
        I = 'Indefinido'
        L = 'Reduzida'
        R = 'Normal'
        H = 'Aumentada'
    
    psychomotor_coordenation: PsychomotorCoordenation = Field(PsychomotorCoordenation.I, title='coordenação psicomotora')
    
    @enummap
    class Rapport(StrEnum):
        I = 'Indefinido'
        L = 'Raport Reduzido'
        R = 'Raport Regular'
        H = 'Raport Intenso'
    
    eye_contact: EyeContact = Field(EyeContact.R, title='contato visutal')
    facial_expression: FacialExpression = Field(FacialExpression.R, title='expressão facial')
    engagement: Engagement = Field(Engagement.R, title='engajamento')
    rapport: Rapport = Field(Rapport.R, title='raport')
    involuntary_movements: Optional[bool] = None
    tremor: OptionalBoolean
    akathisia: OptionalBoolean
    ataxia: OptionalBoolean
    bradykinesia: OptionalBoolean
    tics: OptionalBoolean
    dyskinesia: OptionalBoolean
    maneirisms: OptionalBoolean
    
    @enummap
    class SpeechAmount(StrEnum):
        I = 'Indefinido'
        L = 'Quantidade Reduzida'
        R = 'Quantidade Normal'
        H = 'Quantidade Aumentada'
    
    @enummap
    class SpeechRate(StrEnum):
        I = 'Indefinido'
        L = 'Velocidade Reduzida'
        R = 'Velocidade Normal'
        H = 'Velocidade Aumentada'
    
    @enummap
    class SpeechQuality(StrEnum):
        I = 'Indefinido'
        L = 'Qualidade Empobrecida'
        R = 'Qualidade Regular'
        H = 'Qualidade Elaborada'
    
    @enummap
    class SpeechTone(StrEnum):
        I = 'Indefinido'
        M = 'Tom Monotônico'
        R = 'Tom Natural'
        T = 'Tom Trêmulo'
        C = 'Tom Cantarolante'
        E = 'Tom Estridente'
    
    @enummap
    class SpeechFluence(StrEnum):
        I = 'Indefinido'
        G = 'Fluência Interrompida'
        A = 'Fluência Arrastada'
        P = 'Fluência Artificial'
        R = 'Fluência Regular'
    
    @enummap
    class SpeechVolume(StrEnum):
        I = 'Indefinido'
        L = 'Volume Baixo'
        R = 'Volume Normal'
        H = 'Volume Alto'
    
    speech_amount: SpeechAmount = SpeechAmount.R
    speech_fluency: SpeechFluence = SpeechFluence.R
    speech_rate: SpeechRate = SpeechRate.R
    speech_quality: SpeechQuality = SpeechQuality.R
    speech_volume: SpeechVolume = SpeechVolume.R
    speech_tone: SpeechTone = SpeechTone.R
    
    # Perception
    visual_hallucination: bool = False
    auditory_hallucination: bool = False
    olfactory_hallucination: bool = False
    tactile_hallucination: bool = False
    gustatory_hallucination: bool = False
    despersonalization: bool = False
    desrealization: bool = False
    ilusions: bool = False
    
    # Cognition
    @enummap
    class Alertness(StrEnum):
        I = 'Indefinido'
        N = 'Alerta'
        D = 'Sonolento'
        O = 'Obnubilado'
        S = 'Em Estupor'
        C = 'Comatoso'
    
    alertness: Alertness = Alertness.N
    
    # @enummap
    # class Orientation(StrEnum):
    #     I = 'Indefinido'
    #     N = 'Orientado'
    #     T = 'Desorientado em relação ao Tempo'
    #     L = 'Desorientado em relação ao Espaço'
    #     P = 'Desorientado em relação a Pessoas'
    #     S = 'Desorientado em relação ao Eu'
    #     D = 'Desorientado'
    #
    # orientation: Orientation = Orientation.N
    time_disoriented: OptionalBoolean
    self_disoriented: OptionalBoolean
    person_disoriented: OptionalBoolean
    place_disoriented: OptionalBoolean
    @enummap
    class Attention(StrEnum):
        I = 'Indefinido'
        N = 'Atento'
        L = 'Pouco Desatento'
        M = 'Moderadamente Desatento'
        S = 'Muito Desatento'
        D = 'Totalmente Desatento'
    
    attention: Attention = Attention.N
    
    @enummap
    class Memory(StrEnum):
        I = 'Indefinido'
        N = 'Memória Normal'
        S = 'Memória Imediata Prejudicada'
        R = 'Memória Recente Prejudicada'
        D = 'Memória Tardia Prejudicada'
        L = 'Memória de Longo Prazo Prejudicada'
        G = 'Memória Globalmente Prejudicada'
    
    memory: Memory = Memory.N
    
    @enummap
    class AbstractReasoning(StrEnum):
        I = 'Indefinido'
        N = 'Raciocínio Abstrato Preservado'
        L = 'Raciocínio AbstratoLevemente Prejudicado'
        M = 'Raciocínio Abstrato Moderadamente Prejudicado'
        H = 'Raciocínio AbstratoMuito Prejudicado'
        G = 'Raciocínio Literal'
    
    abstract_reasoning: AbstractReasoning = AbstractReasoning.N
    
    @enummap
    class Tenacity(StrEnum):
        I = 'Indefinido'
        L = 'Hipotenaz'
        N = 'Normotenaz'
        H = 'Hipertenaz'
    
    @enummap
    class Vigilance(StrEnum):
        I = 'Indefinido'
        L = 'Hipovigil'
        N = 'Normovigil'
        H = 'Hipervigil'
    
    @enummap
    class Intellect(StrEnum):
        I = 'Indefinido'
        N = 'Normal'
        L = 'Capacidade Intelectiva Reduzida'
        M = 'Capacidade Intelectiva Muito Reduzida'
        H = 'Capacidade Intelectiva Elevada'
    
    intellect: Intellect = Intellect.N
    
    # MOOD and AFFECT
    mood: Optional[str] = Field(None, title='Humor')
    
    @enummap
    class MoodQuality(StrEnum):
        I = 'Indefinido'
        EUT = 'Eutímico'
        LOW = 'Rebaixado'
        DIS = 'Distímico'
        DEP = 'Depressivo'
        EXP = 'Expansivo'
        HEU = 'Hipomaníaco'
        EUP = 'Eufórico'
        MAN = 'Maníaco'
        ANX = 'Ansioso'
        ANG = 'Irritável'
        ENR = 'Irado'
        GUI = 'Culposo'
        APA = 'Apático'
        PER = 'Perplexo'
        DES = 'Desesperançoso'
        EMP = 'Vazio'
    
    @enummap
    class AffectQuality(StrEnum):
        I = 'Indefinido'
        N = 'Eutímico'
        H = 'Feliz'
        S = 'Triste'
        R = 'Raivoso'
        X = 'Agitado'
        Z = 'Bizarro'
        A = 'Ansioso'
        E = 'Exaltado'
        M = 'Eufórico'
        D = 'Disfórico'
        B = 'Embotado'
    
    affect_quality: AffectQuality = AffectQuality.I
    
    @enummap
    class AffectRange(StrEnum):
        I = 'Indefinido'
        F = 'Fixo'
        N = 'Normal'
        L = 'Lábil'
        A = 'Amplo'
        C = 'Constrito'
        E = 'Embotado'
        
    affect_range: AffectRange = AffectRange.I
    
    @enummap
    class AffectCongruency(StrEnum):
        I = 'Indefinido'
        P = 'Congruente'
        N = 'Incongruente'
    
    affect_congruency: AffectCongruency = AffectCongruency.I
    
    @enummap
    class ThoughtConcept(StrEnum):
        """
        ALTERAÇÕES DOS CONCEITOS
        CONCEITOS: se formam a partir das representações; não apresentam elementos sensoriais, não é possível senti-los ou imaginá-los. Exprimem-se apenas os caracteres mais gerais dos objetos e dos fenômenos.
        Desintegração dos conceitos: conceitos sofrem um processo de perda de seu significado original, uma mesma palavra passa a ter significados cada vez mais diversos (esquizofrenia, síndromes demenciais).
        Condensação dos conceitos: o paciente involuntariamente condensa várias ideias em um único conceito, que se expressa por uma nova palavra (neologismo).
        """
        I = 'Indefinido'
        L = 'Conceitos do Pensamento Desintegrados'
        N = 'Conceitos do Pensamento Adequados'
        H = 'Conceitos do Pensamento Condensados'
        
    thought_concept: ThoughtConcept = ThoughtConcept.I
    
    @enummap
    class ThoughtFlow(StrEnum):
        I = 'Indefinido'
        NOR = 'Normal'
        LOA = 'Perda de Associações'
        CIR = 'Circunstancial'
        TAN = 'Tangencial'
        FLI = 'Fuga de Idéias'
    
    @enummap
    class ThoughtContent(StrEnum):
        I = 'Indefinido'
        R = 'Normal'
        O = 'Obsessivo'
        H = 'Idéias Supervalorizadas'
        D = 'Delirante'
        C = 'Desorganizado'
        
    @enummap
    class SuicidalThought(StrEnum):
        I = 'Indefinido'
        A = 'Ausente'
        S = 'Pensamento Suicida'
        P = 'Planejamento Suicida'
        
    suicidal_thought: SuicidalThought = SuicidalThought.I
    
    notes: Optional[str] = None
    
    
    def __str__(self):
        with io.StringIO() as buf:
            buf.write(f'{self.created} {self.daytime.value}: ')
            for k, v in self.model_fields.items():
                if item:= getattr(self, k):
                    if isinstance(item, StrEnum):
                        if not item.name == 'I':
                            buf.write(f"{item.value}, ")
                    elif v.annotation in [bool, Optional[bool]]:
                        buf.write(f"{v.title}, ")
                    elif v.annotation in [str, Optional[str]] and k is not 'notes':
                        buf.write(f"{item}, ")
            buf.write(f'{self.notes or ""}.')
            return buf.getvalue().lower()
 

@modelmap
class Visit(PactientKeyBase):
    SINGULAR = 'Visita'
    created: DateTimeField = Field(title='Início da Visita')
    complaints: str = Field(title='Queixa Principal')
    intro: Optional[str] = Field(None, title='Introdução')
    subjective: Optional[str] = Field(None, title='Sintomas')
    objective: Optional[str] = Field(None, title='Exame Médico')
    assessment: Optional[str] = Field(None, title='Avaliação')
    plan: Optional[str] = Field(None, title='Plano Terapêutico')
    end: DateTimeField = Field(title='Fim da Visita')
    
    def markup(self):
        with io.StringIO() as buf:
            buf.write(f'#### Visita {self.created.date()}\n')
            buf.write(f'Motivo Principal: **{self.complaints}**\n')
            if self.intro:
                buf.write(f'''
##### HDA
{self.intro}''')
            if self.subjective:
                buf.write(f'Sintomas: {self.subjective}\n')
            if self.objective:
                buf.write(f'Exame: {self.objective}\n')
            if self.assessment:
                buf.write(f'''
##### Análise
{self.assessment}''')
            if self.plan:
                buf.write(f'''
##### Plano Terapêutico
{self.plan}''')
            return Markup(markdown(buf.getvalue()))
    
    def __lt__(self, other):
        return self.created.date() < other.created.date()
    
    def __str__(self):
        return f'{self.created.date()} {self.complaints}'
        
    


